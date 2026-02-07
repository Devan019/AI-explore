"""Frontend agent for analyzing UI/Frontend components."""

from typing import List
from .base_agent import BaseClusterAgent


class FrontendAgent(BaseClusterAgent):
    """Agent specialized in analyzing Frontend/UI code."""

    CLUSTER_NAME = "Frontend"

    FOCUS_AREAS = [
        "Component architecture",
        "State management",
        "Routing structure",
        "API integration",
        "Styling approach",
        "Build configuration"
    ]

    KEY_FILE_PATTERNS = [
        "app", "index", "layout", "page", "component",
        "store", "route", "hook", "context", "provider"
    ]

    def get_system_prompt(self) -> str:
        return """You are an expert Frontend Developer.

Your expertise includes:
- React, Vue, Angular, Svelte
- Next.js, Nuxt.js, Gatsby
- State management (Redux, Zustand, Pinia, MobX)
- Styling (Tailwind, Styled Components, CSS Modules)
- TypeScript in frontend applications
- API integration (REST, GraphQL)
- Build tools (Vite, Webpack, esbuild)

When analyzing code, focus on:
1. Framework and its version
2. Component structure and patterns (atomic design, etc.)
3. State management approach
4. Routing configuration
5. API/data fetching patterns
6. Styling methodology
7. Key pages and their purpose

Provide documentation including:
- Tech stack overview
- Project structure explanation
- How to run development server
- Key components and their relationships
- Route map (if applicable)
- Component diagram (Mermaid)"""

    def select_important_files(self, files: List[dict], max_files: int = 15) -> List[str]:
        """Prioritize Frontend-specific files."""
        selected = []

        # Priority 1: Entry points and configs
        priority_files = [
            "package.json", "app.tsx", "app.jsx", "App.vue", "main.tsx",
            "main.ts", "index.tsx", "index.ts", "_app.tsx", "layout.tsx",
            "tailwind.config.js", "vite.config.ts", "next.config.js"
        ]
        for file in files:
            if file["name"] in priority_files:
                selected.append(file["path"])

        # Priority 2: Page/route files
        for file in files:
            path = file["path"].lower()
            if "/pages/" in path or "/app/" in path or "/routes/" in path:
                if file["path"] not in selected:
                    selected.append(file["path"])

        # Priority 3: Store/state files
        for file in files:
            name = file["name"].lower()
            if "store" in name or "context" in name or "hook" in name:
                if file["path"] not in selected:
                    selected.append(file["path"])

        # Priority 4: Key components
        for file in files:
            path = file["path"].lower()
            if "/components/" in path:
                if file["path"] not in selected:
                    selected.append(file["path"])

        # Fill with remaining
        for file in files:
            if len(selected) >= max_files:
                break
            if file["path"] not in selected:
                selected.append(file["path"])

        return selected[:max_files]
