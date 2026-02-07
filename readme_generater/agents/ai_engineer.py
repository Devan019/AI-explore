"""AI Engineer agent for analyzing AI/LLM components."""

from typing import List
from .base_agent import BaseClusterAgent


class AIEngineerAgent(BaseClusterAgent):
    """Agent specialized in analyzing AI/LLM code."""

    CLUSTER_NAME = "AI_Engineer"

    FOCUS_AREAS = [
        "LLM integrations",
        "Agent architectures",
        "RAG pipelines",
        "Prompt engineering",
        "Embeddings and vector stores",
        "Chat interfaces",
        "Model inference"
    ]

    KEY_FILE_PATTERNS = [
        "agent", "llm", "chat", "prompt", "embed",
        "rag", "chain", "model", "inference", "predict"
    ]

    def get_system_prompt(self) -> str:
        return """You are an expert AI/ML Engineer specializing in LLM applications.

Your expertise includes:
- LangChain, LlamaIndex, and other LLM frameworks
- RAG (Retrieval Augmented Generation) systems
- Agent architectures (ReAct, multi-agent systems)
- Prompt engineering and optimization
- Vector databases (Pinecone, Chroma, Weaviate)
- OpenAI, Anthropic, Groq, and other LLM providers

When analyzing code, focus on:
1. The LLM provider and model being used
2. Agent/chain architecture pattern
3. How context/memory is managed
4. RAG implementation details (if any)
5. Tool/function calling patterns
6. Prompt templates and their purpose

Provide clear, technical documentation suitable for a README."""

    def select_important_files(self, files: List[dict], max_files: int = 15) -> List[str]:
        """Prioritize AI-specific files."""
        selected = []

        # Priority 1: Agent and LLM files
        priority_keywords = ["agent", "llm", "chain",
                             "prompt", "rag", "embed", "chat", "model"]
        for file in files:
            name = file["name"].lower()
            if any(kw in name for kw in priority_keywords):
                selected.append(file["path"])

        # Priority 2: Config files
        for file in files:
            name = file["name"].lower()
            if "config" in name or name.endswith(".yaml") or name.endswith(".yml"):
                if file["path"] not in selected:
                    selected.append(file["path"])

        # Fill with remaining
        for file in files:
            if len(selected) >= max_files:
                break
            if file["path"] not in selected:
                selected.append(file["path"])

        return selected[:max_files]
