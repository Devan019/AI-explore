"""Database agent for analyzing data layer components."""

from typing import List
from .base_agent import BaseClusterAgent


class DatabaseAgent(BaseClusterAgent):
    """Agent specialized in analyzing Database/Data layer code."""

    CLUSTER_NAME = "Database"

    FOCUS_AREAS = [
        "Schema design",
        "ORM models",
        "Migrations",
        "Query patterns",
        "Indexing strategy",
        "Data relationships"
    ]

    KEY_FILE_PATTERNS = [
        "schema", "model", "migration", "entity", "database",
        "seed", "prisma", "knex", "sequelize"
    ]

    def get_system_prompt(self) -> str:
        return """You are an expert Database Engineer and Data Architect.

Your expertise includes:
- SQL databases (PostgreSQL, MySQL, SQLite)
- NoSQL databases (MongoDB, Redis, Elasticsearch)
- ORMs (Prisma, Sequelize, TypeORM, SQLAlchemy, Drizzle)
- Schema design and normalization
- Query optimization and indexing
- Migrations and versioning
- Data modeling patterns

When analyzing code, focus on:
1. Database type and ORM used
2. Schema/model definitions
3. Entity relationships (1:1, 1:N, M:N)
4. Migration strategy
5. Indexes defined
6. Query patterns and complexity
7. Seeding/fixtures

Provide documentation including:
- Database type and configuration
- Data models with relationships
- Migration commands
- Seeding instructions
- Entity-Relationship diagram (Mermaid)"""

    def select_important_files(self, files: List[dict], max_files: int = 15) -> List[str]:
        """Prioritize Database-specific files."""
        selected = []

        # Priority 1: Schema files
        schema_names = ["schema.prisma",
                        "schema.sql", "init.sql", "database.sql"]
        for file in files:
            if file["name"] in schema_names:
                selected.append(file["path"])

        # Priority 2: Model/Entity files
        for file in files:
            name = file["name"].lower()
            path = file["path"].lower()
            if "model" in name or "entity" in name or "/models/" in path or "/entities/" in path:
                if file["path"] not in selected:
                    selected.append(file["path"])

        # Priority 3: Migration files
        for file in files:
            path = file["path"].lower()
            if "/migration" in path:
                if file["path"] not in selected:
                    selected.append(file["path"])

        # Priority 4: Seed files
        for file in files:
            name = file["name"].lower()
            path = file["path"].lower()
            if "seed" in name or "/seeds/" in path:
                if file["path"] not in selected:
                    selected.append(file["path"])

        # Priority 5: Config files
        for file in files:
            name = file["name"].lower()
            if "database" in name or "db" in name or "knex" in name:
                if file["path"] not in selected:
                    selected.append(file["path"])

        # Fill with remaining
        for file in files:
            if len(selected) >= max_files:
                break
            if file["path"] not in selected:
                selected.append(file["path"])

        return selected[:max_files]
