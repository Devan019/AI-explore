"""Backend agent for analyzing server-side components."""

from typing import List
from .base_agent import BaseClusterAgent


class BackendAgent(BaseClusterAgent):
    """Agent specialized in analyzing Backend/API code."""

    CLUSTER_NAME = "Backend"

    FOCUS_AREAS = [
        "API architecture",
        "Route definitions",
        "Database integration",
        "Authentication/Authorization",
        "Middleware patterns",
        "Service layer"
    ]

    KEY_FILE_PATTERNS = [
        "server", "app", "main", "route", "controller",
        "service", "middleware", "handler", "api"
    ]

    def get_system_prompt(self) -> str:
        return """You are an expert Backend Developer.

Your expertise includes:
- Node.js (Express, Fastify, NestJS)
- Python (FastAPI, Flask, Django)
- Go (Gin, Echo, Fiber)
- Java (Spring Boot)
- Rust (Actix, Axum)
- REST API design and GraphQL
- Authentication (JWT, OAuth, sessions)
- Database integration (SQL, NoSQL)

When analyzing code, focus on:
1. Framework and architecture pattern (MVC, Clean Architecture, etc.)
2. API routes and endpoints
3. Authentication/authorization implementation
4. Database models and ORM usage
5. Middleware pipeline
6. Error handling patterns
7. Request validation

Provide documentation including:
- API overview and base URL
- Authentication method
- Key endpoints with methods
- Request/response examples
- Environment variables needed
- API flow diagram (Mermaid)"""

    def select_important_files(self, files: List[dict], max_files: int = 15) -> List[str]:
        """Prioritize Backend-specific files."""
        selected = []

        # Priority 1: Entry points
        entry_points = [
            "server.js", "server.ts", "app.py", "main.py", "main.go",
            "index.js", "index.ts", "Application.java", "Program.cs"
        ]
        for file in files:
            if file["name"] in entry_points:
                selected.append(file["path"])

        # Priority 2: Route files
        for file in files:
            path = file["path"].lower()
            name = file["name"].lower()
            if "/routes/" in path or "/api/" in path or "route" in name:
                if file["path"] not in selected:
                    selected.append(file["path"])

        # Priority 3: Controllers/handlers
        for file in files:
            path = file["path"].lower()
            name = file["name"].lower()
            if "/controllers/" in path or "/handlers/" in path or "controller" in name:
                if file["path"] not in selected:
                    selected.append(file["path"])

        # Priority 4: Middleware
        for file in files:
            name = file["name"].lower()
            if "middleware" in name or "auth" in name:
                if file["path"] not in selected:
                    selected.append(file["path"])

        # Priority 5: Services
        for file in files:
            path = file["path"].lower()
            if "/services/" in path:
                if file["path"] not in selected:
                    selected.append(file["path"])

        # Fill with remaining
        for file in files:
            if len(selected) >= max_files:
                break
            if file["path"] not in selected:
                selected.append(file["path"])

        return selected[:max_files]
