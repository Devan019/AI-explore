import os
import httpx
import base64
import json
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
    ".pptx", ".mp4", ".avi", ".mkv", ".mp3", ".wav", ".flac", ".ogg", ".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg",
    ".psd", ".ai", ".eps", ".ttf", ".woff", ".woff2", ".eot", ".ico", ".zip", ".tar.gz", ".tar", ".rar", ".7z", ".exe", ".dll", ".so", ".bin", ".iso", ".img", ".pdf", ".docx", ".xlsx", ".pptx", ".mp4", ".avi", ".mkv", ".mp3", ".wav", ".flac", ".ogg", ".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".psd", ".ai", ".eps", ".ttf", ".woff", ".woff2", ".eot", ".ico", ".log", ".tmp", ".temp", ".cache", "tsconfig.json", "package-lock.json", "yarn.lock", "pnpm-lock.yaml", "postcss.config.mjs", "tailwind.config.mjs", "webpack.config.js", "babel.config.js", ".eslintrc.json", ".prettierrc", ".editorconfig", ".gitignore", ".dockerignore", "Dockerfile", "Makefile", "CMakeLists.txt", "README.md", "LICENSE", "CHANGELOG.md", "CONTRIBUTING.md", "next.config.ts", "middleware.ts"
}


def _traverse_repo_recursive(owner: str, repo: str, path: str = "") -> list:
    """Internal recursive function for traversing repo."""
    url = f"{GITHUB_API}/repos/{owner}/{repo}/contents/{path}"
    res = httpx.get(url, headers=get_headers())

    if res.status_code != 200:
        return []

    tree = []

    for item in res.json():
        name = item["name"]

        # if item["type"] == "dir" and name in IGNORE_FOLDERS:
        #     continue

        if item["type"] == "file" and any(name.endswith(ext) for ext in IGNORE_EXTENSIONS):
            continue

        node = {
            "name": name,
            "path": item["path"],
            "type": item["type"]
        }

        if item["type"] == "dir":
            node["children"] = _traverse_repo_recursive(
                owner, repo, item["path"])

        tree.append(node)

    return tree


@tool
def traverse_repo(owner: str, repo: str) -> str:
    """
    Traverse a GitHub repository and return its file/folder structure.

    Args:
        owner: The GitHub username or organization that owns the repository
        repo: The name of the repository

    Returns:
        JSON string containing the repository tree structure with files and directories
    """
    tree = _traverse_repo_recursive(owner, repo)
    return json.dumps(tree, indent=2)


def _build_structure_summary_internal(tree: list) -> list:
    """Internal function to build structure summary from tree."""
    summary = []

    for node in tree:
        if node["type"] == "dir":
            summary.append({
                "directory": node["path"],
                "files": [c["name"] for c in node.get("children", []) if c["type"] == "file"],
                "subdirs": [c["name"] for c in node.get("children", []) if c["type"] == "dir"]
            })

    return summary


@tool
def build_structure_summary(owner: str, repo: str) -> str:
    """
    Traverse a GitHub repository and build a summary of its structure.

    Args:
        owner: The GitHub username or organization that owns the repository
        repo: The name of the repository

    Returns:
        JSON string containing a summary with directories, their files, and subdirectories
    """
    tree = _traverse_repo_recursive(owner, repo)
    summary = _build_structure_summary_internal(tree)
    return json.dumps(summary, indent=2)


@tool
def fetch_file_content(owner: str, repo: str, path: str) -> str:
    """
    Fetch the content of a specific file from a GitHub repository.

    Args:
        owner: The GitHub username or organization that owns the repository
        repo: The name of the repository
        path: The path to the file within the repository

    Returns:
        The content of the file as a string, or an error message if fetch fails
    """
    url = f"{GITHUB_API}/repos/{owner}/{repo}/contents/{path}"
    res = httpx.get(url, headers=get_headers())

    if res.status_code != 200:
        return f"Error: Failed to fetch file (status {res.status_code})"

    data = res.json()
    if "content" in data:
        return base64.b64decode(data["content"]).decode("utf-8", errors="ignore")

    return "Error: No content found in response"


@tool
def fetch_multiple_files(owner: str, repo: str, paths_json: str) -> str:
    """
    Fetch contents of multiple files from a GitHub repository.

    Args:
        owner: The GitHub username or organization that owns the repository
        repo: The name of the repository
        paths_json: JSON array of file paths to fetch

    Returns:
        JSON object mapping file paths to their contents
    """
    paths = json.loads(paths_json)
    contents = {}

    for path in paths:
        url = f"{GITHUB_API}/repos/{owner}/{repo}/contents/{path}"
        res = httpx.get(url, headers=get_headers())

        if res.status_code == 200:
            data = res.json()
            if "content" in data:
                contents[path] = base64.b64decode(
                    data["content"]).decode("utf-8", errors="ignore")
            else:
                contents[path] = "Error: No content found"
        else:
            contents[path] = f"Error: Failed to fetch (status {res.status_code})"

    return json.dumps(contents, indent=2)


# Export tools list for easy access
tools = [traverse_repo, build_structure_summary,
         fetch_file_content, fetch_multiple_files]


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
# INTERNAL HELPER FUNCTIONS
# =====================================================
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


def _get_repo_info(owner: str, repo: str) -> dict:
    """Fetch basic repository information."""
    url = f"{GITHUB_API}/repos/{owner}/{repo}"
    res = httpx.get(url, headers=get_headers())
    if res.status_code == 200:
        return res.json()
    return {}


def _extract_files_and_folders(tree: list, files: list = None, folders: list = None) -> tuple:
    """Extract all file names and folder names from tree structure."""
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


def _parse_dependencies(owner: str, repo: str) -> list:
    """Parse dependencies from common package files."""
    dependencies = []

    # Try package.json (Node.js)
    package_json = _fetch_file_raw(owner, repo, "package.json")
    if package_json:
        try:
            data = json.loads(package_json)
            deps = list(data.get("dependencies", {}).keys())
            dev_deps = list(data.get("devDependencies", {}).keys())
            dependencies.extend(deps + dev_deps)
        except:
            pass

    # Try requirements.txt (Python)
    requirements = _fetch_file_raw(owner, repo, "requirements.txt")
    if requirements:
        for line in requirements.split("\n"):
            line = line.strip()
            if line and not line.startswith("#"):
                # Extract package name (before ==, >=, etc.)
                pkg = line.split("==")[0].split(">=")[0].split("<=")[
                    0].split("[")[0].strip()
                if pkg:
                    dependencies.append(pkg.lower())

    # Try pyproject.toml (Python)
    pyproject = _fetch_file_raw(owner, repo, "pyproject.toml")
    if pyproject:
        # Simple parsing for dependencies
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

    # Try Cargo.toml (Rust)
    cargo = _fetch_file_raw(owner, repo, "Cargo.toml")
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

    # Try go.mod (Go)
    gomod = _fetch_file_raw(owner, repo, "go.mod")
    if gomod:
        for line in gomod.split("\n"):
            if line.strip() and not line.startswith("module") and not line.startswith("go "):
                parts = line.strip().split()
                if parts:
                    dependencies.append(parts[0].split("/")[-1].lower())

    return list(set(dependencies))


def _fetch_file_raw(owner: str, repo: str, path: str) -> str | None:
    """Fetch raw file content."""
    url = f"{GITHUB_API}/repos/{owner}/{repo}/contents/{path}"
    res = httpx.get(url, headers=get_headers())
    if res.status_code == 200:
        data = res.json()
        if "content" in data:
            return base64.b64decode(data["content"]).decode("utf-8", errors="ignore")
    return None


def _calculate_cluster_scores(languages: dict, topics: list, files: list, folders: list, dependencies: list) -> dict:
    """Calculate matching scores for each cluster."""
    scores = {}

    # Normalize languages to lowercase
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

        # Check languages (weight: 2)
        for lang in patterns["languages"]:
            if lang.lower() in lang_names:
                score += 2
                matches["languages"].append(lang)

        # Check topics (weight: 3)
        for topic in patterns["topics"]:
            if topic.lower() in topics_lower:
                score += 3
                matches["topics"].append(topic)

        # Check files (weight: 2)
        for f in patterns["files"]:
            if f.lower() in files:
                score += 2
                matches["files"].append(f)

        # Check folders (weight: 2)
        for folder in patterns["folders"]:
            if folder.lower() in folders:
                score += 2
                matches["folders"].append(folder)

        # Check dependencies (weight: 3)
        for dep in patterns["dependencies"]:
            if dep.lower() in deps_lower:
                score += 3
                matches["dependencies"].append(dep)

        scores[cluster_name] = {
            "score": score,
            "matches": matches
        }

    return scores


# =====================================================
# CLUSTERING TOOLS
# =====================================================
@tool
def get_repo_languages(owner: str, repo: str) -> str:
    """
    Get the programming languages used in a GitHub repository.

    Args:
        owner: The GitHub username or organization that owns the repository
        repo: The name of the repository

    Returns:
        JSON string with languages and their byte counts
    """
    languages = _get_repo_languages(owner, repo)
    return json.dumps(languages, indent=2)


@tool
def get_repo_topics(owner: str, repo: str) -> str:
    """
    Get the topics/tags associated with a GitHub repository.

    Args:
        owner: The GitHub username or organization that owns the repository
        repo: The name of the repository

    Returns:
        JSON array of topic names
    """
    topics = _get_repo_topics(owner, repo)
    return json.dumps(topics, indent=2)


@tool
def get_repo_dependencies(owner: str, repo: str) -> str:
    """
    Parse and extract dependencies from a GitHub repository.
    Supports package.json, requirements.txt, pyproject.toml, Cargo.toml, go.mod.

    Args:
        owner: The GitHub username or organization that owns the repository
        repo: The name of the repository

    Returns:
        JSON array of dependency names
    """
    dependencies = _parse_dependencies(owner, repo)
    return json.dumps(dependencies, indent=2)


@tool
def classify_repo(owner: str, repo: str) -> str:
    """
    Analyze a GitHub repository and classify it into tech clusters.

    Clusters: AI_Engineer, ML_Engineer, DevOps, Frontend, Backend, Web3, Database

    Args:
        owner: The GitHub username or organization that owns the repository
        repo: The name of the repository

    Returns:
        JSON object with cluster classifications, scores, and matched patterns
    """
    # Gather all data
    languages = _get_repo_languages(owner, repo)
    topics = _get_repo_topics(owner, repo)
    tree = _traverse_repo_recursive(owner, repo)
    files, folders = _extract_files_and_folders(tree)
    dependencies = _parse_dependencies(owner, repo)
    repo_info = _get_repo_info(owner, repo)

    # Calculate scores
    scores = _calculate_cluster_scores(
        languages, topics, files, folders, dependencies)

    # Sort clusters by score
    sorted_clusters = sorted(
        scores.items(), key=lambda x: x[1]["score"], reverse=True)

    # Get primary and secondary classifications
    primary = None
    secondary = []

    for cluster_name, data in sorted_clusters:
        if data["score"] > 0:
            if primary is None:
                primary = cluster_name
            else:
                secondary.append(cluster_name)

    result = {
        "repository": f"{owner}/{repo}",
        "description": repo_info.get("description", ""),
        "primary_cluster": primary,
        "secondary_clusters": secondary[:3],  # Top 3 secondary clusters
        "languages": languages,
        "topics": topics,
        "dependencies_found": len(dependencies),
        "cluster_scores": {k: v for k, v in sorted_clusters if v["score"] > 0}
    }

    return json.dumps(result, indent=2)


@tool
def batch_classify_repos(repos_json: str) -> str:
    """
    Classify multiple GitHub repositories into tech clusters.

    Args:
        repos_json: JSON array of objects with 'owner' and 'repo' keys
                    Example: [{"owner": "facebook", "repo": "react"}]

    Returns:
        JSON array of classification results for each repository
    """
    repos = json.loads(repos_json)
    results = []

    for r in repos:
        owner = r.get("owner")
        repo = r.get("repo")
        if owner and repo:
            try:
                classification = json.loads(
                    classify_repo.invoke({"owner": owner, "repo": repo}))
                results.append(classification)
            except Exception as e:
                results.append({
                    "repository": f"{owner}/{repo}",
                    "error": str(e)
                })

    return json.dumps(results, indent=2)


# Update tools list
tools = [
    traverse_repo,
    build_structure_summary,
    fetch_file_content,
    fetch_multiple_files,
    get_repo_languages,
    get_repo_topics,
    get_repo_dependencies,
    classify_repo,
    batch_classify_repos
]
