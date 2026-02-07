"""Base agent class for cluster-specific agents."""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
import json

from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, SystemMessage

from ..utils import tools, fetch_file_content, fetch_multiple_files
from ..config import get_agent_config


class BaseClusterAgent(ABC):
    """Base class for all cluster-specific agents."""

    CLUSTER_NAME: str = "Base"

    # Override in subclasses with specific focus areas
    FOCUS_AREAS: List[str] = []
    KEY_FILE_PATTERNS: List[str] = []

    def __init__(
        self,
        model_name: str = None,
        provider: str = None,
        api_key: str = None
    ):
        # Get config for this agent, use provided values or fall back to config
        config = get_agent_config(self.CLUSTER_NAME)

        self._model_name = model_name or config["model"]
        self._provider = provider or config["provider"]
        self._api_key = api_key or config["api_key"]

        # Build model kwargs with api_key if provided
        model_kwargs = {
            "model": self._model_name,
            "model_provider": self._provider,
            "temperature": 0.2
        }

        # Add API key based on provider
        if self._api_key:
            if self._provider == "groq":
                model_kwargs["api_key"] = self._api_key
            elif self._provider == "openai":
                model_kwargs["api_key"] = self._api_key
            elif self._provider in ["google_genai", "google-genai"]:
                model_kwargs["api_key"] = self._api_key

        self.model = init_chat_model(**model_kwargs)
        self.model_with_tools = self.model.bind_tools(tools)

    @abstractmethod
    def get_system_prompt(self) -> str:
        """Return the system prompt for this agent."""
        pass

    def select_important_files(self, files: List[Dict], max_files: int = 15) -> List[str]:
        """
        Select the most important files to analyze.
        Override in subclasses for custom selection logic.
        """
        selected = []

        # Priority 1: Key file patterns
        for file in files:
            name = file["name"].lower()
            path = file["path"].lower()

            for pattern in self.KEY_FILE_PATTERNS:
                if pattern.lower() in name or pattern.lower() in path:
                    if file["path"] not in selected:
                        selected.append(file["path"])
                    break

        # Priority 2: Entry points and configs
        priority_names = ["main", "index", "app",
                          "server", "config", "__init__"]
        for file in files:
            name = file["name"].lower().split(".")[0]
            if name in priority_names and file["path"] not in selected:
                selected.append(file["path"])

        # Fill remaining with other files
        for file in files:
            if len(selected) >= max_files:
                break
            if file["path"] not in selected:
                selected.append(file["path"])

        return selected[:max_files]

    def analyze(self, owner: str, repo: str, cluster_data: Dict) -> Dict[str, Any]:
        """
        Analyze the cluster and generate documentation.

        Args:
            owner: GitHub owner
            repo: Repository name
            cluster_data: Data for this cluster including files, matches, etc.

        Returns:
            ClusterAnalysis dict
        """
        files = cluster_data.get("files", [])
        matches = cluster_data.get("matches", {})

        if not files:
            return {
                "cluster_name": self.CLUSTER_NAME,
                "summary": f"No {self.CLUSTER_NAME} files found in this repository.",
                "key_files": [],
                "technologies": [],
                "architecture": "",
                "features": [],
                "setup_steps": [],
                "diagrams": None
            }

        # Select important files
        important_files = self.select_important_files(files, max_files=25)

        # Fetch file contents (increased limit for better analysis)
        file_contents = {}
        for path in important_files[:20]:  # Fetch max 20 files
            content = fetch_file_content.invoke({
                "owner": owner,
                "repo": repo,
                "path": path
            })
            if content and not content.startswith("Error"):
                # Increased truncation limit for more context
                file_contents[path] = content[:12000] if len(
                    content) > 12000 else content

        # Get project context for additional info
        project_context = cluster_data.get("project_context", {})

        # Build analysis prompt
        analysis_prompt = self._build_analysis_prompt(
            owner=owner,
            repo=repo,
            files=files,
            matches=matches,
            file_contents=file_contents,
            project_context=project_context
        )

        # Get analysis from LLM
        system_prompt = self.get_system_prompt()

        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=analysis_prompt)
        ]

        response = self.model.invoke(messages)

        # Parse response
        return self._parse_response(response.content, files, matches)

    def _build_analysis_prompt(
        self,
        owner: str,
        repo: str,
        files: List[Dict],
        matches: Dict,
        file_contents: Dict[str, str],
        project_context: Dict[str, Any] = None
    ) -> str:
        """Build the analysis prompt."""
        project_context = project_context or {}

        # Show more files for better context
        file_list = "\n".join([f"- {f['path']}" for f in files[:50]])

        contents_str = ""
        for path, content in file_contents.items():
            contents_str += f"\n\n### {path}\n```\n{content}\n```"

        # Add project context section
        context_str = ""
        if project_context.get("repo_description"):
            context_str += f"**Repository Description**: {project_context['repo_description']}\n\n"
        if project_context.get("readme"):
            # Include relevant parts of existing README
            readme_preview = project_context["readme"][:3000]
            context_str += f"**Existing README (preview)**:\n{readme_preview}\n\n"

        return f"""
Analyze the {self.CLUSTER_NAME} components of this repository.

## Repository: {owner}/{repo}
{context_str}
## Matched Patterns
- Languages: {', '.join(matches.get('languages', [])) or 'None'}
- Dependencies: {', '.join(matches.get('dependencies', [])) or 'None'}
- Key Files: {', '.join(matches.get('files', [])) or 'None'}
- Folders: {', '.join(matches.get('folders', [])) or 'None'}

## Files in this cluster ({len(files)} total)
{file_list}

## File Contents
{contents_str if contents_str else "No file contents available"}

## Your Task
Analyze the code and provide:

1. **Summary**: 2-3 sentences describing what this part of the codebase does
2. **Key Files**: List the most important files and their purpose
3. **Technologies**: List specific frameworks/libraries used
4. **Architecture**: Describe the architecture pattern (if identifiable)
5. **Features**: List main features/capabilities
6. **Setup Steps**: Commands/steps needed for this part
7. **Diagram**: If applicable, provide a Mermaid diagram (flowchart/sequence)

Respond in JSON format:
```json
{{
    "summary": "...",
    "key_files": [{{"path": "...", "purpose": "..."}}],
    "technologies": ["..."],
    "architecture": "...",
    "features": ["..."],
    "setup_steps": ["..."],
    "diagram": "```mermaid\\n...\\n```" or null
}}
```
"""

    def _parse_response(
        self,
        response: str,
        files: List[Dict],
        matches: Dict
    ) -> Dict[str, Any]:
        """Parse LLM response into ClusterAnalysis format."""

        try:
            # Try to extract JSON from response
            json_start = response.find("{")
            json_end = response.rfind("}") + 1

            if json_start != -1 and json_end > json_start:
                json_str = response[json_start:json_end]
                data = json.loads(json_str)

                return {
                    "cluster_name": self.CLUSTER_NAME,
                    "summary": data.get("summary", ""),
                    "key_files": [f["path"] if isinstance(f, dict) else f for f in data.get("key_files", [])],
                    "technologies": data.get("technologies", []),
                    "architecture": data.get("architecture", ""),
                    "features": data.get("features", []),
                    "setup_steps": data.get("setup_steps", []),
                    "diagrams": data.get("diagram")
                }
        except (json.JSONDecodeError, KeyError):
            pass

        # Fallback: return basic info
        return {
            "cluster_name": self.CLUSTER_NAME,
            "summary": response[:500] if response else f"Analysis of {self.CLUSTER_NAME} components",
            "key_files": [f["path"] for f in files[:5]],
            "technologies": matches.get("dependencies", []),
            "architecture": "",
            "features": [],
            "setup_steps": [],
            "diagrams": None
        }
