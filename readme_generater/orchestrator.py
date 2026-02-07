"""Orchestrator - coordinates all agents and generates final README."""

import logging
import os
from typing import Dict, Any, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed

from .utils import get_cluster_data, render_all_diagrams
from .State import RepoState
from .config import get_agent_config, AGENT_CONFIGS
from .agents import (
    CLUSTER_AGENTS,
    ReadmeAggregatorAgent
)

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)
log = logging.getLogger("README_GENERATOR")


class ReadmeOrchestrator:
    """
    Orchestrates the multi-agent README generation process.

    Each agent uses its own model and API key from config.py.
    Configure per-agent settings in config.py or via environment variables.

    Flow:
    1. Fetch repository data and cluster files
    2. Run cluster agents in parallel (each with own model/key)
    3. Aggregate results and generate final README
    """

    def __init__(self, max_workers: int = 4):
        """
        Initialize the orchestrator.

        Args:
            max_workers: Maximum parallel agents (default: 4)
        """
        self.max_workers = max_workers

        # Initialize agents lazily
        self._cluster_agents = {}
        self._aggregator = None

    def _get_cluster_agent(self, cluster_name: str):
        """Get or create a cluster agent using its config."""
        if cluster_name not in self._cluster_agents:
            agent_class = CLUSTER_AGENTS.get(cluster_name)
            if agent_class:
                # Agent will use its own config from config.py
                self._cluster_agents[cluster_name] = agent_class()
        return self._cluster_agents.get(cluster_name)

    def _get_aggregator(self):
        """Get or create the aggregator agent using its config."""
        if self._aggregator is None:
            # Aggregator will use its own config from config.py
            self._aggregator = ReadmeAggregatorAgent()
        return self._aggregator

    def generate(self, owner: str, repo: str) -> str:
        """
        Generate a comprehensive README for a GitHub repository.

        Args:
            owner: GitHub username or organization
            repo: Repository name

        Returns:
            Complete README.md content
        """
        log.info(f"🚀 Starting README generation for {owner}/{repo}")

        # Step 1: Get cluster data
        log.info("📊 Fetching repository data and clustering files...")
        cluster_data = get_cluster_data(owner, repo)

        log.info(f"📁 Total files: {cluster_data['total_files']}")
        log.info(
            f"🏷️  Languages: {', '.join(cluster_data['languages'].keys())}")
        log.info(
            f"📦 Active clusters: {', '.join(cluster_data['clusters'].keys())}")

        # Step 2: Run cluster agents in parallel
        log.info("🤖 Running cluster agents in parallel...")
        agent_outputs = self._run_cluster_agents_parallel(
            owner, repo, cluster_data)

        active_outputs = {k: v for k, v in agent_outputs.items(
        ) if v and not v.get("summary", "").startswith("No ")}
        log.info(
            f"✅ Completed analyses for: {', '.join(active_outputs.keys())}")

        # Step 3: Render mermaid diagrams to images
        log.info("🎨 Rendering mermaid diagrams to images...")
        rendered_diagrams = render_all_diagrams(
            agent_outputs, output_dir="diagrams")
        if rendered_diagrams:
            log.info(f"📊 Rendered {len(rendered_diagrams)} diagram(s)")
        else:
            log.info("📊 No mermaid diagrams found to render")

        # Step 4: Aggregate and generate README
        log.info("📝 Generating final README...")
        repo_info = {
            "owner": owner,
            "repo": repo,
            "languages": cluster_data["languages"],
            "topics": cluster_data["topics"],
            "dependencies": cluster_data["dependencies"],
            "project_context": cluster_data.get("project_context", {}),
            "rendered_diagrams": rendered_diagrams,
            "folder_structure": cluster_data.get("folder_structure", "")
        }

        aggregator = self._get_aggregator()
        readme = aggregator.generate_readme(repo_info, agent_outputs)

        log.info("🎉 README generation complete!")

        return readme

    def _run_cluster_agents_parallel(
        self,
        owner: str,
        repo: str,
        cluster_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Run all cluster agents in parallel."""

        clusters = cluster_data.get("clusters", {})
        results = {}

        def analyze_cluster(cluster_name: str) -> tuple:
            """Worker function for parallel execution."""
            try:
                agent = self._get_cluster_agent(cluster_name)
                if agent is None:
                    log.warning(
                        f"⚠️  No agent found for cluster: {cluster_name}")
                    return cluster_name, None

                log.info(f"🔍 Analyzing {cluster_name}...")
                cluster_info = clusters.get(cluster_name, {})
                # Pass project context for better analysis
                cluster_info["project_context"] = cluster_data.get(
                    "project_context", {})
                result = agent.analyze(owner, repo, cluster_info)
                log.info(f"✅ {cluster_name} analysis complete")
                return cluster_name, result
            except Exception as e:
                log.error(f"❌ Error analyzing {cluster_name}: {e}")
                return cluster_name, {
                    "cluster_name": cluster_name,
                    "summary": f"Error during analysis: {str(e)}",
                    "key_files": [],
                    "technologies": [],
                    "architecture": "",
                    "features": [],
                    "setup_steps": [],
                    "diagrams": None
                }

        # Run in parallel
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = {
                executor.submit(analyze_cluster, cluster_name): cluster_name
                for cluster_name in clusters.keys()
            }

            for future in as_completed(futures):
                cluster_name, result = future.result()
                results[cluster_name] = result

        return results

    def generate_to_file(
        self,
        owner: str,
        repo: str,
        output_path: str = "README.md"
    ) -> str:
        """
        Generate README and save to file.

        Args:
            owner: GitHub username or organization
            repo: Repository name
            output_path: Output file path

        Returns:
            Path to the generated file
        """
        readme = self.generate(owner, repo)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(readme)

        log.info(f"📄 README saved to: {output_path}")
        return output_path


def generate_readme(owner: str, repo: str, output_path: Optional[str] = None) -> str:
    """
    Convenience function to generate README.

    Args:
        owner: GitHub username or organization
        repo: Repository name
        output_path: Optional output file path

    Returns:
        README content (also saves to file if output_path provided)
    """
    orchestrator = ReadmeOrchestrator()

    if output_path:
        orchestrator.generate_to_file(owner, repo, output_path)
        with open(output_path, "r", encoding="utf-8") as f:
            return f.read()

    return orchestrator.generate(owner, repo)


# CLI entry point
if __name__ == "__main__":

    owner = "Devan019"
    repo = "smartscout"
    output = f"{repo}_README.md"

    readme = generate_readme(owner, repo, output)
    print(f"\n{'='*60}")
    print(f"README generated successfully!")
    print(f"Output: {output}")
    print(f"{'='*60}")
