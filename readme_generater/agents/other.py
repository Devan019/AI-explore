"""Other agent for analyzing miscellaneous components."""

from typing import List
from .base_agent import BaseClusterAgent


class OtherAgent(BaseClusterAgent):
    """Agent specialized in analyzing miscellaneous/uncategorized code."""

    CLUSTER_NAME = "Other"

    FOCUS_AREAS = [
        "Utility functions",
        "Configuration",
        "Scripts",
        "Documentation",
        "Testing"
    ]

    KEY_FILE_PATTERNS = [
        "util", "helper", "config", "setup", "test",
        "script", "tool", "common", "shared"
    ]

    def get_system_prompt(self) -> str:
        return """You are an expert Software Engineer with broad knowledge.

Your task is to analyze code that doesn't fit neatly into other categories.

Focus on:
1. Utility functions and helpers
2. Configuration patterns
3. Testing setup
4. Build scripts
5. Documentation
6. Common/shared code

When analyzing code, identify:
1. The purpose of each file
2. Reusable utilities or helpers
3. Configuration options
4. Testing approach
5. Any scripts and their purpose

Provide documentation including:
- Overview of miscellaneous components
- Key utilities and their purpose
- Configuration options
- Scripts and their usage"""

    def select_important_files(self, files: List[dict], max_files: int = 15) -> List[str]:
        """Select important miscellaneous files."""
        selected = []

        # Priority 1: Config files
        config_patterns = ["config", "settings",
                           "env", ".json", ".yaml", ".yml"]
        for file in files:
            name = file["name"].lower()
            if any(p in name for p in config_patterns):
                selected.append(file["path"])

        # Priority 2: Utility files
        for file in files:
            name = file["name"].lower()
            if "util" in name or "helper" in name or "common" in name:
                if file["path"] not in selected:
                    selected.append(file["path"])

        # Priority 3: Test files
        for file in files:
            name = file["name"].lower()
            path = file["path"].lower()
            if "test" in name or "/tests/" in path:
                if file["path"] not in selected:
                    selected.append(file["path"])

        # Fill with remaining
        for file in files:
            if len(selected) >= max_files:
                break
            if file["path"] not in selected:
                selected.append(file["path"])

        return selected[:max_files]
