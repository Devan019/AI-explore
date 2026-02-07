"""
README Generator - Multi-agent system for generating comprehensive README files.

Usage:
    from readme_generater import generate_readme
    
    # Generate README for a GitHub repo
    readme = generate_readme("owner", "repo")
    
    # Or save directly to file
    readme = generate_readme("owner", "repo", "README.md")
    
Configure per-agent API keys:
    from readme_generater import set_agent_config, set_all_api_keys
    
    # Set different keys for different agents
    set_agent_config("AI_Engineer", api_key="your-key-1")
    set_agent_config("Frontend", api_key="your-key-2")
    
    # Or set same key for all agents
    set_all_api_keys("your-groq-key")
"""

from .utils import (
    get_repo_clusters,
    get_clustered_files,
    get_cluster_data,
    CLUSTER_PATTERNS,
    tools,
    # Mermaid diagram rendering
    render_mermaid_to_url,
    render_mermaid_to_file,
    render_all_diagrams,
    extract_mermaid_diagrams
)

from .State import RepoState, ClusterInfo, ClusterAnalysis

from .orchestrator import (
    ReadmeOrchestrator,
    generate_readme
)

from .config import (
    AGENT_CONFIGS,
    get_agent_config,
    set_agent_config,
    set_all_api_keys
)

__all__ = [
    # Main function
    "generate_readme",
    "ReadmeOrchestrator",

    # Config functions
    "AGENT_CONFIGS",
    "get_agent_config",
    "set_agent_config",
    "set_all_api_keys",

    # Utility functions
    "get_repo_clusters",
    "get_clustered_files",
    "get_cluster_data",

    # Mermaid rendering
    "render_mermaid_to_url",
    "render_mermaid_to_file",
    "render_all_diagrams",
    "extract_mermaid_diagrams",

    # Types
    "RepoState",
    "ClusterInfo",
    "ClusterAnalysis",

    # Constants
    "CLUSTER_PATTERNS",
    "tools"
]
