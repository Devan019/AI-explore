"""
Configuration for per-agent model and API keys.

Each agent can have its own:
- model: The model name (e.g., "llama-3.3-70b-versatile")
- provider: LLM provider (e.g., "groq", "openai", "google_genai")
- api_key: API key for this agent's provider

Usage:
    # Set your API keys here or via environment variables
    AGENT_CONFIGS["AI_Engineer"]["api_key"] = "your-key-here"
"""

import os
from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file

# Default configuration (used if agent-specific config not found)
DEFAULT_CONFIG = {
    "model": "llama-3.3-70b-versatile",
    "provider": "groq",
    "api_key": os.getenv("GROQ_API_KEY", ""),
}

# Per-agent configurations
# Each agent can have different model, provider, and API key
AGENT_CONFIGS = {
    "AI_Engineer": {
        "model": "llama-3.3-70b-versatile",
        "provider": "groq",
        "api_key": os.getenv("GROQ_API_KEY_AI_ENGINEER", os.getenv("GROQ_API_KEY", "")),
    },
    "ML_Engineer": {
        "model": "llama-3.3-70b-versatile",
        "provider": "groq",
        "api_key": os.getenv("GROQ_API_KEY_ML_ENGINEER", os.getenv("GROQ_API_KEY", "")),
    },
    "DevOps": {
        "model": "llama-3.3-70b-versatile",
        "provider": "groq",
        "api_key": os.getenv("GROQ_API_KEY_DEVOPS", os.getenv("GROQ_API_KEY", "")),
    },
    "Frontend": {
        "model": "llama-3.3-70b-versatile",
        "provider": "groq",
        "api_key": os.getenv("GROQ_API_KEY_FRONTEND", os.getenv("GROQ_API_KEY", "")),
    },
    "Backend": {
        "model": "llama-3.3-70b-versatile",
        "provider": "groq",
        "api_key": os.getenv("GROQ_API_KEY_BACKEND", os.getenv("GROQ_API_KEY", "")),
    },
    "Web3": {
        "model": "llama-3.3-70b-versatile",
        "provider": "groq",
        "api_key": os.getenv("GROQ_API_KEY_WEB3", os.getenv("GROQ_API_KEY", "")),
    },
    "Database": {
        "model": "llama-3.3-70b-versatile",
        "provider": "groq",
        "api_key": os.getenv("GROQ_API_KEY_DATABASE", os.getenv("GROQ_API_KEY", "")),
    },
    "Other": {
        "model": "llama-3.3-70b-versatile",
        "provider": "groq",
        "api_key": os.getenv("GROQ_API_KEY_OTHER", os.getenv("GROQ_API_KEY", "")),
    },
    # Aggregator agent (combines all outputs)
    "Aggregator": {
        "model": "llama-3.3-70b-versatile",
        "provider": "groq",
        "api_key": os.getenv("GROQ_API_KEY_AGGREGATOR", os.getenv("GROQ_API_KEY", "")),
    },
}


def get_agent_config(agent_name: str) -> dict:
    """
    Get configuration for a specific agent.
    Falls back to DEFAULT_CONFIG if agent not found.
    """
    return AGENT_CONFIGS.get(agent_name, DEFAULT_CONFIG.copy())


def set_agent_config(agent_name: str, model: str = None, provider: str = None, api_key: str = None):
    """
    Update configuration for a specific agent.

    Example:
        set_agent_config("AI_Engineer", api_key="sk-xxx")
        set_agent_config("Frontend", model="gpt-4", provider="openai", api_key="sk-xxx")
    """
    if agent_name not in AGENT_CONFIGS:
        AGENT_CONFIGS[agent_name] = DEFAULT_CONFIG.copy()

    if model is not None:
        AGENT_CONFIGS[agent_name]["model"] = model
    if provider is not None:
        AGENT_CONFIGS[agent_name]["provider"] = provider
    if api_key is not None:
        AGENT_CONFIGS[agent_name]["api_key"] = api_key


def set_all_api_keys(api_key: str):
    """Set the same API key for all agents."""
    for agent_name in AGENT_CONFIGS:
        AGENT_CONFIGS[agent_name]["api_key"] = api_key
