"""DevOps agent for analyzing infrastructure and CI/CD components."""

from typing import List
from .base_agent import BaseClusterAgent


class DevOpsAgent(BaseClusterAgent):
    """Agent specialized in analyzing DevOps/Infrastructure code."""

    CLUSTER_NAME = "DevOps"

    FOCUS_AREAS = [
        "Docker containerization",
        "Kubernetes orchestration",
        "CI/CD pipelines",
        "Infrastructure as Code",
        "Cloud deployments",
        "Monitoring and logging"
    ]

    KEY_FILE_PATTERNS = [
        "Dockerfile", "docker-compose", "kubernetes", "k8s",
        "terraform", "ansible", "jenkins", "workflow", "deploy",
        "helm", "chart", "pipeline"
    ]

    def get_system_prompt(self) -> str:
        return """You are an expert DevOps Engineer and SRE.

Your expertise includes:
- Docker and container orchestration
- Kubernetes (deployments, services, ingress)
- Terraform, Pulumi for Infrastructure as Code
- CI/CD with GitHub Actions, Jenkins, GitLab CI
- Cloud platforms (AWS, GCP, Azure)
- Helm charts and package management
- Monitoring (Prometheus, Grafana)

When analyzing code, focus on:
1. Container configuration and multi-stage builds
2. Kubernetes resource definitions
3. CI/CD pipeline stages and triggers
4. Infrastructure provisioning steps
5. Environment variables and secrets management
6. Deployment strategies (rolling, blue-green)
7. Health checks and monitoring setup

Provide clear documentation including:
- How to build and run containers
- Deployment prerequisites
- Environment setup
- CI/CD workflow explanation
- Infrastructure diagram (Mermaid)"""

    def select_important_files(self, files: List[dict], max_files: int = 15) -> List[str]:
        """Prioritize DevOps-specific files."""
        selected = []

        # Priority 1: Core infrastructure files
        priority_files = [
            "Dockerfile", "docker-compose.yml", "docker-compose.yaml",
            "main.tf", "variables.tf", "deployment.yaml", "service.yaml",
            "Chart.yaml", "values.yaml", "Jenkinsfile"
        ]
        for file in files:
            if file["name"] in priority_files:
                selected.append(file["path"])

        # Priority 2: GitHub workflows
        for file in files:
            if ".github/workflows" in file["path"]:
                if file["path"] not in selected:
                    selected.append(file["path"])

        # Priority 3: Other infra files
        infra_keywords = ["deploy", "k8s", "helm", "terraform", "ansible"]
        for file in files:
            path = file["path"].lower()
            if any(kw in path for kw in infra_keywords):
                if file["path"] not in selected:
                    selected.append(file["path"])

        # Fill with remaining
        for file in files:
            if len(selected) >= max_files:
                break
            if file["path"] not in selected:
                selected.append(file["path"])

        return selected[:max_files]
