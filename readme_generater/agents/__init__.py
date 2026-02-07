from .base_agent import BaseClusterAgent
from .ai_engineer import AIEngineerAgent
from .ml_engineer import MLEngineerAgent
from .devops import DevOpsAgent
from .frontend import FrontendAgent
from .backend import BackendAgent
from .web3 import Web3Agent
from .database import DatabaseAgent
from .other import OtherAgent
from .readme_aggregator import ReadmeAggregatorAgent

CLUSTER_AGENTS = {
    "AI_Engineer": AIEngineerAgent,
    "ML_Engineer": MLEngineerAgent,
    "DevOps": DevOpsAgent,
    "Frontend": FrontendAgent,
    "Backend": BackendAgent,
    "Web3": Web3Agent,
    "Database": DatabaseAgent,
    "Other": OtherAgent
}

__all__ = [
    "BaseClusterAgent",
    "AIEngineerAgent",
    "MLEngineerAgent",
    "DevOpsAgent",
    "FrontendAgent",
    "BackendAgent",
    "Web3Agent",
    "DatabaseAgent",
    "OtherAgent",
    "ReadmeAggregatorAgent",
    "CLUSTER_AGENTS"
]
