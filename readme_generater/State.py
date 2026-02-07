from typing import TypedDict, Dict, Any, List, Optional


class ClusterInfo(TypedDict):
    score: int
    matches: Dict[str, List[str]]
    files: List[Dict[str, str]]
    file_count: int


class ClusterAnalysis(TypedDict):
    """Output from a cluster agent"""
    cluster_name: str
    summary: str
    key_files: List[str]
    technologies: List[str]
    architecture: str
    features: List[str]
    setup_steps: List[str]
    diagrams: Optional[str]  # Mermaid diagrams if applicable


class RepoState(TypedDict):
    # Input
    owner: str
    repo: str

    # Cluster data
    repo_url: str
    languages: Dict[str, int]
    topics: List[str]
    dependencies: List[str]
    clusters: Dict[str, ClusterInfo]
    total_files: int

    # Agent outputs
    agent_outputs: Dict[str, ClusterAnalysis]

    # Final output
    final_readme: str
