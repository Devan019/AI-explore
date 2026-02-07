"""ML Engineer agent for analyzing ML/Data Science components."""

from typing import List
from .base_agent import BaseClusterAgent


class MLEngineerAgent(BaseClusterAgent):
    """Agent specialized in analyzing ML/Data Science code."""

    CLUSTER_NAME = "ML_Engineer"

    FOCUS_AREAS = [
        "Model training pipelines",
        "Data preprocessing",
        "Feature engineering",
        "Model evaluation",
        "Experiment tracking",
        "Model serving"
    ]

    KEY_FILE_PATTERNS = [
        "train", "model", "dataset", "preprocess", "feature",
        "evaluate", "predict", "pipeline", "notebook"
    ]

    def get_system_prompt(self) -> str:
        return """You are an expert ML Engineer and Data Scientist.

Your expertise includes:
- PyTorch, TensorFlow, and Keras
- Scikit-learn and classical ML algorithms
- Data preprocessing with Pandas/NumPy
- Feature engineering techniques
- MLflow, Weights & Biases for experiment tracking
- Model evaluation and validation
- Jupyter notebooks and data exploration

When analyzing code, focus on:
1. Model architecture and type (CNN, Transformer, etc.)
2. Training pipeline structure
3. Data loading and preprocessing steps
4. Feature engineering approach
5. Evaluation metrics used
6. Hyperparameter configuration
7. Model checkpointing and saving

Provide clear documentation including:
- How to prepare data
- How to train the model
- How to run inference
- Key metrics and results (if available)"""

    def select_important_files(self, files: List[dict], max_files: int = 15) -> List[str]:
        """Prioritize ML-specific files."""
        selected = []

        # Priority 1: Training and model files
        priority_keywords = ["train", "model", "dataset", "pipeline", "config"]
        for file in files:
            name = file["name"].lower()
            if any(kw in name for kw in priority_keywords):
                selected.append(file["path"])

        # Priority 2: Notebooks
        for file in files:
            if file["name"].endswith(".ipynb"):
                if file["path"] not in selected:
                    selected.append(file["path"])

        # Priority 3: Requirements/configs
        for file in files:
            name = file["name"].lower()
            if "requirements" in name or "config" in name:
                if file["path"] not in selected:
                    selected.append(file["path"])

        # Fill with remaining
        for file in files:
            if len(selected) >= max_files:
                break
            if file["path"] not in selected:
                selected.append(file["path"])

        return selected[:max_files]
