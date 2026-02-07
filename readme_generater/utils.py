import zlib
import re
import os
import httpx
import base64
import json
from typing import Optional
from dotenv import load_dotenv
from langchain_core.tools import tool

load_dotenv()

GITHUB_API = "https://api.github.com"


def get_headers():
    token = os.getenv("GITHUB_TOKEN")
    return {
        "Authorization": f"token {token}" if token else "",
        "Accept": "application/vnd.github.v3+json"
    }


IGNORE_EXTENSIONS = {
    ".log", ".tmp", ".temp", ".cache", ".zip", ".tar.gz", ".tar", ".rar", ".7z",
    ".exe", ".dll", ".so", ".bin", ".iso", ".img", ".pdf", ".docx", ".xlsx",
    ".pptx", ".mp4", ".avi", ".mkv", ".mp3", ".wav", ".flac", ".ogg", ".jpg",
    ".jpeg", ".png", ".gif", ".bmp", ".svg", ".psd", ".ai", ".eps", ".ttf",
    ".woff", ".woff2", ".eot", ".ico"
}


# =====================================================
# CLUSTER DEFINITIONS
# =====================================================
CLUSTER_PATTERNS = {
    "AI_Engineer": {
        "files": ["model.py", "inference.py", "train.py", "predict.py", "agent.py", "llm.py", "prompt.py", "chat.py", "embeddings.py"],
        "folders": ["models", "agents", "prompts", "llm", "ai", "chatbot"],
        "dependencies": ["openai", "langchain", "langchain-core", "langgraph", "anthropic", "groq", "transformers", "huggingface-hub", "llama-index", "chromadb", "pinecone", "weaviate", "faiss", "sentence-transformers", "tiktoken", "ollama"],
        "languages": ["python", "jupyter notebook"],
        "topics": ["ai", "llm", "gpt", "chatgpt", "langchain", "rag", "agents", "nlp", "chatbot", "generative-ai"]
    },
    "ML_Engineer": {
        "files": ["train.py", "model.py", "dataset.py", "evaluate.py", "preprocess.py", "features.py", "pipeline.py"],
        "folders": ["models", "data", "notebooks", "experiments", "training", "evaluation", "features"],
        "dependencies": ["tensorflow", "torch", "pytorch", "keras", "scikit-learn", "sklearn", "xgboost", "lightgbm", "catboost", "pandas", "numpy", "scipy", "matplotlib", "seaborn", "mlflow", "wandb", "optuna", "ray"],
        "languages": ["python", "jupyter notebook", "r"],
        "topics": ["machine-learning", "deep-learning", "ml", "neural-network", "data-science", "pytorch", "tensorflow", "keras"]
    },
    "DevOps": {
        "files": ["Dockerfile", "docker-compose.yml", "docker-compose.yaml", "Jenkinsfile", ".gitlab-ci.yml", "azure-pipelines.yml", "cloudbuild.yaml", "terraform.tf", "main.tf", "ansible.yml", "playbook.yml", "k8s.yaml", "deployment.yaml", "values.yaml", "Chart.yaml", "Vagrantfile"],
        "folders": ["terraform", "ansible", "kubernetes", "k8s", "helm", "charts", "infra", "infrastructure", ".github/workflows", "ci", "cd", "deploy"],
        "dependencies": ["docker", "kubernetes", "ansible", "terraform", "pulumi", "aws-cdk", "boto3", "azure", "google-cloud"],
        "languages": ["shell", "hcl", "dockerfile"],
        "topics": ["devops", "docker", "kubernetes", "k8s", "ci-cd", "infrastructure", "terraform", "ansible", "aws", "azure", "gcp", "cloud"]
    },
    "Frontend": {
        "files": ["index.html", "app.tsx", "app.jsx", "App.vue", "app.component.ts", "tailwind.config.js", "vite.config.ts", "next.config.js", "nuxt.config.js"],
        "folders": ["components", "pages", "views", "layouts", "styles", "assets", "public", "src/components", "src/pages"],
        "dependencies": ["react", "react-dom", "vue", "angular", "svelte", "next", "nuxt", "gatsby", "vite", "webpack", "tailwindcss", "styled-components", "emotion", "sass", "less", "bootstrap", "material-ui", "@mui", "antd", "chakra-ui", "redux", "zustand", "mobx", "react-query", "tanstack"],
        "languages": ["javascript", "typescript", "css", "scss", "html", "vue"],
        "topics": ["frontend", "react", "vue", "angular", "svelte", "nextjs", "web", "ui", "tailwind", "css"]
    },
    "Backend": {
        "files": ["server.js", "server.ts", "app.py", "main.go", "main.rs", "Application.java", "Program.cs", "routes.py", "controllers.py", "middleware.py"],
        "folders": ["routes", "controllers", "middleware", "services", "api", "handlers", "repositories", "entities"],
        "dependencies": ["express", "fastapi", "flask", "django", "nestjs", "spring", "gin", "echo", "fiber", "actix", "axum", "rocket", "koa", "hapi", "fastify", "graphql", "apollo-server", "prisma", "sequelize", "typeorm", "sqlalchemy", "mongoose"],
        "languages": ["python", "javascript", "typescript", "go", "java", "rust", "c#", "ruby", "php"],
        "topics": ["backend", "api", "rest", "graphql", "server", "microservices", "express", "fastapi", "django", "flask"]
    },
    "Web3": {
        "files": ["hardhat.config.js", "hardhat.config.ts", "truffle-config.js", "foundry.toml", "anchor.toml", "Move.toml"],
        "folders": ["contracts", "scripts", "test", "migrations", "programs"],
        "dependencies": ["ethers", "web3", "hardhat", "truffle", "@openzeppelin", "solmate", "foundry", "@solana/web3.js", "anchor", "wagmi", "viem", "rainbowkit", "thirdweb", "moralis", "alchemy-sdk"],
        "languages": ["solidity", "rust", "move", "vyper"],
        "topics": ["web3", "blockchain", "ethereum", "solana", "smart-contracts", "defi", "nft", "crypto", "solidity", "hardhat"]
    },
    "Database": {
        "files": ["schema.sql", "migrations.sql", "init.sql", "schema.prisma", "models.py", "entities.py"],
        "folders": ["migrations", "seeds", "schemas", "database", "db"],
        "dependencies": ["prisma", "sequelize", "typeorm", "sqlalchemy", "mongoose", "knex", "drizzle", "pg", "mysql2", "mongodb", "redis", "elasticsearch", "neo4j", "cassandra-driver", "psycopg2", "pymongo", "motor"],
        "languages": ["sql", "plpgsql"],
        "topics": ["database", "sql", "nosql", "postgresql", "mysql", "mongodb", "redis", "elasticsearch", "orm"]
    }
}


# =====================================================
# HELPER FUNCTIONS
# =====================================================
def _traverse_repo(owner: str, repo: str, path: str = "") -> list:
    """Recursively traverse repo and get file tree."""
    url = f"{GITHUB_API}/repos/{owner}/{repo}/contents/{path}"
    res = httpx.get(url, headers=get_headers())

    if res.status_code != 200:
        return []

    tree = []
    for item in res.json():
        name = item["name"]

        if item["type"] == "file" and any(name.endswith(ext) for ext in IGNORE_EXTENSIONS):
            continue

        node = {
            "name": name,
            "path": item["path"],
            "type": item["type"]
        }

        if item["type"] == "dir":
            node["children"] = _traverse_repo(owner, repo, item["path"])

        tree.append(node)

    return tree


def _get_repo_languages(owner: str, repo: str) -> dict:
    """Fetch languages used in the repository."""
    url = f"{GITHUB_API}/repos/{owner}/{repo}/languages"
    res = httpx.get(url, headers=get_headers())
    if res.status_code == 200:
        return res.json()
    return {}


def _get_repo_topics(owner: str, repo: str) -> list:
    """Fetch topics/tags of the repository."""
    url = f"{GITHUB_API}/repos/{owner}/{repo}/topics"
    headers = get_headers()
    headers["Accept"] = "application/vnd.github.mercy-preview+json"
    res = httpx.get(url, headers=headers)
    if res.status_code == 200:
        return res.json().get("names", [])
    return []


def _fetch_file(owner: str, repo: str, path: str) -> str | None:
    """Fetch raw file content."""
    url = f"{GITHUB_API}/repos/{owner}/{repo}/contents/{path}"
    res = httpx.get(url, headers=get_headers())
    if res.status_code == 200:
        data = res.json()
        if "content" in data:
            return base64.b64decode(data["content"]).decode("utf-8", errors="ignore")
    return None


def _parse_dependencies(owner: str, repo: str) -> list:
    """Parse dependencies from common package files."""
    dependencies = []

    # package.json (Node.js)
    package_json = _fetch_file(owner, repo, "package.json")
    if package_json:
        try:
            data = json.loads(package_json)
            deps = list(data.get("dependencies", {}).keys())
            dev_deps = list(data.get("devDependencies", {}).keys())
            dependencies.extend(deps + dev_deps)
        except:
            pass

    # requirements.txt (Python)
    requirements = _fetch_file(owner, repo, "requirements.txt")
    if requirements:
        for line in requirements.split("\n"):
            line = line.strip()
            if line and not line.startswith("#"):
                pkg = line.split("==")[0].split(">=")[0].split("<=")[
                    0].split("[")[0].strip()
                if pkg:
                    dependencies.append(pkg.lower())

    # pyproject.toml (Python)
    pyproject = _fetch_file(owner, repo, "pyproject.toml")
    if pyproject:
        in_deps = False
        for line in pyproject.split("\n"):
            if "dependencies" in line.lower() and "=" in line:
                in_deps = True
            elif in_deps:
                if line.strip().startswith("["):
                    in_deps = False
                elif "=" in line or line.strip().startswith('"') or line.strip().startswith("'"):
                    pkg = line.strip().strip('"').strip("'").strip(",").split(">=")[
                        0].split("==")[0].split("[")[0]
                    if pkg and not pkg.startswith("["):
                        dependencies.append(pkg.lower())

    # Cargo.toml (Rust)
    cargo = _fetch_file(owner, repo, "Cargo.toml")
    if cargo:
        in_deps = False
        for line in cargo.split("\n"):
            if "[dependencies]" in line:
                in_deps = True
            elif line.strip().startswith("[") and in_deps:
                in_deps = False
            elif in_deps and "=" in line:
                pkg = line.split("=")[0].strip()
                if pkg:
                    dependencies.append(pkg.lower())

    # go.mod (Go)
    gomod = _fetch_file(owner, repo, "go.mod")
    if gomod:
        for line in gomod.split("\n"):
            if line.strip() and not line.startswith("module") and not line.startswith("go "):
                parts = line.strip().split()
                if parts:
                    dependencies.append(parts[0].split("/")[-1].lower())

    return list(set(dependencies))


def _extract_files_and_folders(tree: list, files: list = None, folders: list = None) -> tuple:
    """Extract all file names and folder names from tree."""
    if files is None:
        files = []
    if folders is None:
        folders = []

    for node in tree:
        if node["type"] == "file":
            files.append(node["name"].lower())
        elif node["type"] == "dir":
            folders.append(node["name"].lower())
            if "children" in node:
                _extract_files_and_folders(node["children"], files, folders)

    return files, folders


def _calculate_cluster_scores(languages: dict, topics: list, files: list, folders: list, dependencies: list) -> dict:
    """Calculate matching scores for each cluster."""
    scores = {}

    lang_names = [lang.lower() for lang in languages.keys()]
    topics_lower = [t.lower() for t in topics]
    deps_lower = [d.lower() for d in dependencies]

    for cluster_name, patterns in CLUSTER_PATTERNS.items():
        score = 0
        matches = {
            "languages": [],
            "topics": [],
            "files": [],
            "folders": [],
            "dependencies": []
        }

        for lang in patterns["languages"]:
            if lang.lower() in lang_names:
                score += 2
                matches["languages"].append(lang)

        for topic in patterns["topics"]:
            if topic.lower() in topics_lower:
                score += 3
                matches["topics"].append(topic)

        for f in patterns["files"]:
            if f.lower() in files:
                score += 2
                matches["files"].append(f)

        for folder in patterns["folders"]:
            if folder.lower() in folders:
                score += 2
                matches["folders"].append(folder)

        for dep in patterns["dependencies"]:
            if dep.lower() in deps_lower:
                score += 3
                matches["dependencies"].append(dep)

        scores[cluster_name] = {
            "score": score,
            "matches": matches
        }

    return scores


def _classify_file(file_path: str, file_name: str) -> str:
    """Classify a single file into a cluster using smart heuristics."""
    name_lower = file_name.lower()
    path_lower = file_path.lower()
    ext = os.path.splitext(name_lower)[1]
    name_no_ext = os.path.splitext(name_lower)[0]

    # Priority 1: Exact file name matches
    for cluster_name, patterns in CLUSTER_PATTERNS.items():
        if name_lower in [f.lower() for f in patterns["files"]]:
            return cluster_name

    # Priority 2: Folder-based classification
    for cluster_name, patterns in CLUSTER_PATTERNS.items():
        for folder in patterns["folders"]:
            folder_lower = folder.lower()
            if f"/{folder_lower}/" in f"/{path_lower}/" or path_lower.startswith(f"{folder_lower}/"):
                return cluster_name

    # Priority 3: Extension-based (strong indicators)
    strong_ext_mapping = {
        ".sol": "Web3", ".vy": "Web3", ".move": "Web3",
        ".prisma": "Database",
        ".tf": "DevOps", ".hcl": "DevOps",
        ".vue": "Frontend", ".svelte": "Frontend",
        ".ipynb": "ML_Engineer",
    }
    if ext in strong_ext_mapping:
        return strong_ext_mapping[ext]

    # Priority 4: Pattern matching in file names
    ai_patterns = ["agent", "llm", "chat", "prompt",
                   "embed", "rag", "chain", "inference", "predict"]
    ml_patterns = ["train", "model", "dataset", "preprocess",
                   "feature", "evaluate", "pipeline", "neural"]
    devops_patterns = ["deploy", "docker", "jenkins",
                       "terraform", "ansible", "k8s", "helm", "ci", "cd"]
    frontend_patterns = ["component", "page", "view",
                         "layout", "style", "hook", "context", "store"]
    backend_patterns = ["controller", "route", "handler",
                        "service", "middleware", "repository", "api", "server"]
    web3_patterns = ["contract", "token",
                     "nft", "mint", "stake", "swap", "vault"]
    db_patterns = ["migration", "schema", "seed", "entity", "model", "query"]

    if any(p in name_no_ext for p in ai_patterns):
        return "AI_Engineer"
    if any(p in name_no_ext for p in ml_patterns):
        return "ML_Engineer"
    if any(p in name_no_ext for p in devops_patterns):
        return "DevOps"
    if any(p in name_no_ext for p in web3_patterns):
        return "Web3"
    if any(p in name_no_ext for p in db_patterns):
        return "Database"

    # Priority 5: Path-based patterns
    if any(p in path_lower for p in ["/api/", "/routes/", "/controllers/", "/services/", "/handlers/"]):
        return "Backend"
    if any(p in path_lower for p in ["/components/", "/pages/", "/views/", "/ui/", "/styles/"]):
        return "Frontend"
    if any(p in path_lower for p in ["/agents/", "/llm/", "/prompts/", "/chains/"]):
        return "AI_Engineer"
    if any(p in path_lower for p in ["/models/", "/training/", "/notebooks/", "/data/"]):
        return "ML_Engineer"
    if any(p in path_lower for p in ["/contracts/", "/scripts/", "/hardhat/", "/foundry/"]):
        return "Web3"
    if any(p in path_lower for p in ["/migrations/", "/schemas/", "/db/", "/database/"]):
        return "Database"
    if any(p in path_lower for p in ["/.github/", "/infra/", "/deploy/", "/k8s/", "/terraform/"]):
        return "DevOps"

    # Priority 6: Extension + name pattern for ambiguous files
    if ext in [".tsx", ".jsx"]:
        return "Frontend"
    if ext in [".css", ".scss", ".sass", ".less"]:
        return "Frontend"
    if ext in [".html"] and "index" not in name_lower:
        return "Frontend"
    if ext in [".sql"]:
        return "Database"
    if ext in [".yml", ".yaml"]:
        # Check if it's a CI/CD or config file
        if any(p in name_lower for p in ["docker", "compose", "ci", "cd", "deploy", "pipeline", "action"]):
            return "DevOps"
        return "Other"

    # Priority 7: Backend indicators for .py, .js, .ts files
    if ext in [".py", ".js", ".ts", ".go", ".java", ".rs"]:
        if any(p in name_no_ext for p in backend_patterns):
            return "Backend"
        if any(p in name_no_ext for p in frontend_patterns):
            return "Frontend"
        # Default Python files to Backend if not otherwise classified
        if ext == ".py" and "test" not in name_lower:
            return "Backend"
        # Default JS/TS to Frontend unless in api/server folders
        if ext in [".js", ".ts"]:
            if any(p in path_lower for p in ["/server/", "/api/", "/backend/"]):
                return "Backend"
            return "Frontend"

    return "Other"


# =====================================================
# MAIN FUNCTIONS
# =====================================================
def get_repo_clusters(owner: str, repo: str) -> dict:
    """
    Analyze a GitHub repository and classify it into tech clusters.

    Returns dict with:
        - primary_cluster: Main cluster classification
        - secondary_clusters: Other matching clusters
        - cluster_scores: Detailed scores and matches for each cluster
    """
    languages = _get_repo_languages(owner, repo)
    topics = _get_repo_topics(owner, repo)
    tree = _traverse_repo(owner, repo)
    files, folders = _extract_files_and_folders(tree)
    dependencies = _parse_dependencies(owner, repo)

    scores = _calculate_cluster_scores(
        languages, topics, files, folders, dependencies)
    sorted_clusters = sorted(
        scores.items(), key=lambda x: x[1]["score"], reverse=True)

    primary = None
    secondary = []

    for cluster_name, data in sorted_clusters:
        if data["score"] > 0:
            if primary is None:
                primary = cluster_name
            else:
                secondary.append(cluster_name)

    return {
        "primary_cluster": primary,
        "secondary_clusters": secondary,
        "languages": languages,
        "topics": topics,
        "dependencies": dependencies,
        "cluster_scores": {k: v for k, v in sorted_clusters if v["score"] > 0}
    }


def get_clustered_files(owner: str, repo: str) -> dict:
    """
    Get all files from a repository organized by their tech cluster.

    Returns dict with files grouped by cluster:
        - AI_Engineer: [...]
        - Frontend: [...]
        - Backend: [...]
        - etc.
    """
    tree = _traverse_repo(owner, repo)

    clustered = {
        "AI_Engineer": [],
        "ML_Engineer": [],
        "DevOps": [],
        "Frontend": [],
        "Backend": [],
        "Web3": [],
        "Database": [],
        "Other": []
    }

    def process_tree(nodes: list):
        for node in nodes:
            if node["type"] == "file":
                cluster = _classify_file(node["path"], node["name"])
                clustered[cluster].append({
                    "name": node["name"],
                    "path": node["path"]
                })
            elif node["type"] == "dir" and "children" in node:
                process_tree(node["children"])

    process_tree(tree)

    # Remove empty clusters
    return {k: v for k, v in clustered.items() if v}


# =====================================================
# ENHANCED CLUSTERING WITH URLS
# =====================================================
def _get_project_context(owner: str, repo: str) -> dict:
    """Fetch key project files for better context."""
    context = {
        "readme": None,
        "package_json": None,
        "requirements_txt": None,
        "pyproject_toml": None,
        "repo_description": None
    }

    # Try to get README
    for readme_name in ["README.md", "readme.md", "README.rst", "README"]:
        content = _fetch_file(owner, repo, readme_name)
        if content:
            context["readme"] = content[:8000]  # First 8000 chars
            break

    # Get package.json
    package_json = _fetch_file(owner, repo, "package.json")
    if package_json:
        context["package_json"] = package_json

    # Get requirements.txt
    requirements = _fetch_file(owner, repo, "requirements.txt")
    if requirements:
        context["requirements_txt"] = requirements

    # Get pyproject.toml
    pyproject = _fetch_file(owner, repo, "pyproject.toml")
    if pyproject:
        context["pyproject_toml"] = pyproject

    # Get repo description
    url = f"{GITHUB_API}/repos/{owner}/{repo}"
    res = httpx.get(url, headers=get_headers())
    if res.status_code == 200:
        data = res.json()
        context["repo_description"] = data.get("description", "")

    return context


def _classify_file_multi(file_path: str, file_name: str) -> list:
    """
    Classify a file into potentially multiple clusters.
    Returns list of cluster names the file belongs to.
    """
    clusters = []
    primary = _classify_file(file_path, file_name)
    clusters.append(primary)

    name_lower = file_name.lower()
    path_lower = file_path.lower()
    name_no_ext = os.path.splitext(name_lower)[0]

    # Cross-cluster keywords
    cross_cluster_indicators = {
        "AI_Engineer": ["agent", "llm", "chat", "prompt", "embed", "rag", "chain", "langchain", "openai"],
        "ML_Engineer": ["model", "train", "predict", "neural", "tensor", "torch", "sklearn"],
        "Backend": ["api", "route", "controller", "service", "handler", "server"],
        "Frontend": ["component", "page", "view", "hook", "ui", "style"],
        "DevOps": ["docker", "deploy", "ci", "cd", "terraform", "k8s"],
        "Database": ["schema", "migration", "query", "db", "repository"],
        "Web3": ["contract", "token", "mint", "blockchain", "solidity"]
    }

    for cluster, keywords in cross_cluster_indicators.items():
        if cluster != primary:
            if any(kw in name_no_ext or kw in path_lower for kw in keywords):
                clusters.append(cluster)

    return clusters


def get_cluster_data(owner: str, repo: str) -> dict:
    """
    Get comprehensive cluster data including file URLs and metadata.
    Returns all clusters (primary + secondary) with detailed info.
    """
    languages = _get_repo_languages(owner, repo)
    topics = _get_repo_topics(owner, repo)
    tree = _traverse_repo(owner, repo)
    files_list, folders_list = _extract_files_and_folders(tree)
    dependencies = _parse_dependencies(owner, repo)

    # Get project context for better analysis
    project_context = _get_project_context(owner, repo)

    scores = _calculate_cluster_scores(
        languages, topics, files_list, folders_list, dependencies)
    sorted_clusters = sorted(
        scores.items(), key=lambda x: x[1]["score"], reverse=True)

    # Get clustered files with multi-classification
    clustered_files = {
        "AI_Engineer": [],
        "ML_Engineer": [],
        "DevOps": [],
        "Frontend": [],
        "Backend": [],
        "Web3": [],
        "Database": [],
        "Other": []
    }

    # Track files for deduplication within clusters
    seen_in_cluster = {k: set() for k in clustered_files}

    def process_tree_with_urls(nodes: list):
        for node in nodes:
            if node["type"] == "file":
                # Get all applicable clusters for this file
                clusters = _classify_file_multi(node["path"], node["name"])
                file_url = f"https://github.com/{owner}/{repo}/blob/main/{node['path']}"
                raw_url = f"https://raw.githubusercontent.com/{owner}/{repo}/main/{node['path']}"
                file_info = {
                    "name": node["name"],
                    "path": node["path"],
                    "url": file_url,
                    "raw_url": raw_url
                }
                # Add to all applicable clusters
                for cluster in clusters:
                    if node["path"] not in seen_in_cluster[cluster]:
                        clustered_files[cluster].append(file_info)
                        seen_in_cluster[cluster].add(node["path"])
            elif node["type"] == "dir" and "children" in node:
                process_tree_with_urls(node["children"])

    process_tree_with_urls(tree)

    # Build active clusters (score > 0)
    active_clusters = {}
    for cluster_name, data in sorted_clusters:
        if data["score"] > 0 or clustered_files.get(cluster_name):
            active_clusters[cluster_name] = {
                "score": data["score"],
                "matches": data["matches"],
                "files": clustered_files.get(cluster_name, []),
                "file_count": len(clustered_files.get(cluster_name, []))
            }

    # Also include "Other" if it has files
    if clustered_files.get("Other"):
        active_clusters["Other"] = {
            "score": 0,
            "matches": {"languages": [], "topics": [], "files": [], "folders": [], "dependencies": []},
            "files": clustered_files["Other"],
            "file_count": len(clustered_files["Other"])
        }

    return {
        "owner": owner,
        "repo": repo,
        "repo_url": f"https://github.com/{owner}/{repo}",
        "languages": languages,
        "topics": topics,
        "dependencies": dependencies,
        "clusters": active_clusters,
        "total_files": sum(len(files) for files in clustered_files.values()),
        "project_context": project_context,  # README, package.json, etc.
        # Folder structure string
        "folder_structure": _generate_folder_tree(tree)
    }


def _generate_folder_tree(tree: list, prefix: str = "", is_last: bool = True, max_depth: int = 4, current_depth: int = 0) -> str:
    """
    Generate a visual folder tree structure string.

    Args:
        tree: The file tree from _traverse_repo
        prefix: Current line prefix for indentation
        is_last: Whether this is the last item in current level
        max_depth: Maximum depth to traverse
        current_depth: Current depth level

    Returns:
        String representation of folder structure
    """
    if current_depth > max_depth:
        return ""

    lines = []

    # Sort: directories first, then files
    sorted_tree = sorted(tree, key=lambda x: (
        x["type"] != "dir", x["name"].lower()))

    for i, node in enumerate(sorted_tree):
        is_last_item = (i == len(sorted_tree) - 1)
        connector = "└── " if is_last_item else "├── "

        if node["type"] == "dir":
            lines.append(f"{prefix}{connector}{node['name']}/")

            # Generate children with updated prefix
            if "children" in node and node["children"] and current_depth < max_depth:
                extension = "    " if is_last_item else "│   "
                child_tree = _generate_folder_tree(
                    node["children"],
                    prefix + extension,
                    is_last_item,
                    max_depth,
                    current_depth + 1
                )
                if child_tree:
                    lines.append(child_tree)
        else:
            lines.append(f"{prefix}{connector}{node['name']}")

    return "\n".join(lines)


def get_folder_structure(owner: str, repo: str, max_depth: int = 4) -> str:
    """
    Get a visual folder structure for a GitHub repository.

    Args:
        owner: GitHub username or organization
        repo: Repository name
        max_depth: Maximum folder depth to show

    Returns:
        String representation of folder structure
    """
    tree = _traverse_repo(owner, repo)
    structure = _generate_folder_tree(tree, max_depth=max_depth)
    return f"{repo}/\n{structure}"


# =====================================================
# TOOLS FOR AGENTS
# =====================================================
@tool
def fetch_file_content(owner: str, repo: str, path: str) -> str:
    """
    Fetch the content of a specific file from a GitHub repository.
    Use this to read file contents when you need to analyze code.

    Args:
        owner: GitHub username or organization
        repo: Repository name
        path: File path in the repo (e.g., "src/app.py")

    Returns:
        File content as string, or error message
    """
    content = _fetch_file(owner, repo, path)
    if content:
        return content
    return f"Error: Could not fetch {path}"


@tool
def fetch_multiple_files(owner: str, repo: str, paths: list[str]) -> dict:
    """
    Fetch contents of multiple files at once.
    More efficient than fetching one by one.

    Args:
        owner: GitHub username or organization
        repo: Repository name
        paths: List of file paths to fetch

    Returns:
        Dict mapping path to content
    """
    results = {}
    for path in paths[:20]:  # Limit to 20 files
        content = _fetch_file(owner, repo, path)
        results[path] = content if content else f"Error: Could not fetch {path}"
    return results


@tool
def list_directory(owner: str, repo: str, path: str = "") -> list:
    """
    List contents of a directory in the repository.

    Args:
        owner: GitHub username or organization
        repo: Repository name
        path: Directory path (empty for root)

    Returns:
        List of files and folders in the directory
    """
    url = f"{GITHUB_API}/repos/{owner}/{repo}/contents/{path}"
    res = httpx.get(url, headers=get_headers())

    if res.status_code != 200:
        return []

    items = []
    for item in res.json():
        items.append({
            "name": item["name"],
            "path": item["path"],
            "type": item["type"],
            "size": item.get("size", 0)
        })
    return items


@tool
def search_in_repo(owner: str, repo: str, query: str) -> list:
    """
    Search for code in the repository.

    Args:
        owner: GitHub username or organization
        repo: Repository name
        query: Search query (code, filename, etc.)

    Returns:
        List of matching files with paths
    """
    url = f"{GITHUB_API}/search/code?q={query}+repo:{owner}/{repo}"
    headers = get_headers()
    headers["Accept"] = "application/vnd.github.v3.text-match+json"
    res = httpx.get(url, headers=headers)

    if res.status_code != 200:
        return []

    results = []
    for item in res.json().get("items", [])[:15]:
        results.append({
            "name": item["name"],
            "path": item["path"],
            "url": item["html_url"]
        })
    return results


# Export tools for agents
tools = [fetch_file_content, fetch_multiple_files,
         list_directory, search_in_repo]


# =====================================================
# MERMAID DIAGRAM RENDERING
# =====================================================


def _clean_mermaid_code(mermaid_code: str) -> str:
    """Clean up mermaid code by removing code block markers."""
    mermaid_code = mermaid_code.strip()
    if mermaid_code.startswith("```mermaid"):
        mermaid_code = mermaid_code[10:]
    if mermaid_code.startswith("```"):
        mermaid_code = mermaid_code[3:]
    if mermaid_code.endswith("```"):
        mermaid_code = mermaid_code[:-3]
    return mermaid_code.strip()


def _encode_mermaid_base64(mermaid_code: str) -> str:
    """Encode mermaid code using simple base64 for mermaid.ink API."""
    mermaid_code = _clean_mermaid_code(mermaid_code)
    encoded = base64.b64encode(mermaid_code.encode('utf-8')).decode('utf-8')
    return encoded


def render_mermaid_to_url(mermaid_code: str, theme: str = "default") -> str:
    """
    Convert Mermaid code to an image URL using mermaid.ink service.

    Args:
        mermaid_code: Mermaid diagram code
        theme: Theme for the diagram (default, dark, forest, neutral)

    Returns:
        URL to the rendered image
    """
    # Use simple base64 encoding (more reliable)
    encoded = _encode_mermaid_base64(mermaid_code)
    return f"https://mermaid.ink/img/{encoded}?theme={theme}"


def render_mermaid_to_file(mermaid_code: str, output_path: str, theme: str = "default", fix_with_llm: bool = True) -> str:
    """
    Render Mermaid diagram to a local image file.
    If rendering fails (400 error), optionally use LLM to fix the mermaid code.

    Args:
        mermaid_code: Mermaid diagram code
        output_path: Path to save the image (e.g., "diagrams/architecture.png")
        theme: Theme for the diagram
        fix_with_llm: Whether to try fixing with LLM on 400 error

    Returns:
        Path to the saved image, or error message
    """
    try:
        url = render_mermaid_to_url(mermaid_code, theme)
        response = httpx.get(url, timeout=30.0)

        if response.status_code == 200:
            # Ensure directory exists
            os.makedirs(os.path.dirname(output_path) if os.path.dirname(
                output_path) else ".", exist_ok=True)

            # Save the image
            with open(output_path, "wb") as f:
                f.write(response.content)

            return output_path
        elif response.status_code == 400 and fix_with_llm:
            # Try to fix the mermaid code with LLM
            fixed_code = _fix_mermaid_with_llm(mermaid_code)
            if fixed_code and fixed_code != mermaid_code:
                # Try again with fixed code (but don't recurse infinitely)
                return render_mermaid_to_file(fixed_code, output_path, theme, fix_with_llm=False)
            return f"Error: Failed to render diagram (HTTP 400 - invalid mermaid syntax)"
        else:
            return f"Error: Failed to render diagram (HTTP {response.status_code})"
    except Exception as e:
        return f"Error: {str(e)}"


def _fix_mermaid_with_llm(mermaid_code: str) -> str:
    """
    Use LLM to fix invalid mermaid code.

    Args:
        mermaid_code: The broken mermaid code

    Returns:
        Fixed mermaid code, or original if fix failed
    """
    try:
        from langchain.chat_models import init_chat_model
        from langchain_core.messages import HumanMessage, SystemMessage
        from .config import get_agent_config

        config = get_agent_config("Aggregator")

        model = init_chat_model(
            model=config["model"],
            model_provider=config["provider"],
            api_key=config["api_key"] if config["api_key"] else None,
            temperature=0.1
        )

        system_prompt = """You are a Mermaid diagram syntax expert. Fix the invalid Mermaid code provided.

Common issues to fix:
- Missing or extra brackets
- Invalid node names (use alphanumeric, no special chars in IDs)
- Incorrect arrow syntax (use --> or ---)
- Missing quotes around labels with special characters
- Invalid direction (use TB, TD, LR, RL, BT)
- Subgraph syntax errors

Return ONLY the corrected mermaid code, no explanation, no markdown code blocks."""

        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=f"Fix this mermaid code:\n\n{mermaid_code}")
        ]

        response = model.invoke(messages)
        fixed = response.content.strip()

        # Clean up response
        if fixed.startswith("```"):
            fixed = fixed.split("\n", 1)[1] if "\n" in fixed else fixed[3:]
        if fixed.endswith("```"):
            fixed = fixed[:-3]

        return fixed.strip()
    except Exception as e:
        # If LLM fix fails, return original
        return mermaid_code


def extract_mermaid_diagrams(text: str) -> list:
    """
    Extract all mermaid diagram code blocks from text.

    Args:
        text: Text containing mermaid code blocks

    Returns:
        List of mermaid code strings
    """
    patterns = [
        r'```mermaid\s*([\s\S]*?)```',
        r'```\s*(graph\s+[A-Z]{2}[\s\S]*?)```',
        r'```\s*(flowchart\s+[A-Z]{2}[\s\S]*?)```',
        r'```\s*(sequenceDiagram[\s\S]*?)```',
        r'```\s*(classDiagram[\s\S]*?)```',
        r'```\s*(stateDiagram[\s\S]*?)```',
        r'```\s*(erDiagram[\s\S]*?)```',
        r'```\s*(gantt[\s\S]*?)```',
        r'```\s*(pie[\s\S]*?)```',
    ]

    diagrams = []
    for pattern in patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        diagrams.extend(matches)

    return [d.strip() for d in diagrams if d.strip()]


def render_all_diagrams(agent_outputs: dict, output_dir: str = "diagrams") -> dict:
    """
    Extract and render all mermaid diagrams from agent outputs.

    Args:
        agent_outputs: Dict of cluster_name -> analysis results
        output_dir: Directory to save diagram images

    Returns:
        Dict mapping diagram names to their image paths
    """
    rendered = {}
    diagram_count = 0

    for cluster_name, analysis in agent_outputs.items():
        if not analysis:
            continue

        diagrams_text = analysis.get("diagrams", "")
        if not diagrams_text:
            continue

        # Extract mermaid code blocks
        mermaid_codes = extract_mermaid_diagrams(diagrams_text)

        for i, code in enumerate(mermaid_codes):
            diagram_count += 1
            # Generate filename
            safe_cluster = cluster_name.replace(" ", "_").lower()
            filename = f"{output_dir}/{safe_cluster}_diagram_{i+1}.png"

            # Render to file
            result = render_mermaid_to_file(code, filename)

            if not result.startswith("Error"):
                diagram_key = f"{cluster_name}_{i+1}"
                rendered[diagram_key] = {
                    "path": result,
                    "code": code,
                    "cluster": cluster_name
                }

    return rendered
