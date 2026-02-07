"""README Aggregator agent - combines all cluster analyses into final README."""

from typing import Dict, Any, List
import json

from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, SystemMessage

from ..config import get_agent_config


class ReadmeAggregatorAgent:
    """Agent that aggregates all cluster analyses into a comprehensive README."""

    def __init__(
        self,
        model_name: str = None,
        provider: str = None,
        api_key: str = None
    ):
        # Get config for aggregator, use provided values or fall back to config
        config = get_agent_config("Aggregator")

        self._model_name = model_name or config["model"]
        self._provider = provider or config["provider"]
        self._api_key = api_key or config["api_key"]

        # Build model kwargs with api_key if provided
        model_kwargs = {
            "model": self._model_name,
            "model_provider": self._provider,
            "temperature": 0.3
        }

        # Add API key based on provider
        if self._api_key:
            if self._provider == "groq":
                model_kwargs["api_key"] = self._api_key
            elif self._provider == "openai":
                model_kwargs["api_key"] = self._api_key
            elif self._provider in ["google_genai", "google-genai"]:
                model_kwargs["api_key"] = self._api_key

        self.model = init_chat_model(**model_kwargs)

    def get_system_prompt(self) -> str:
        return """You are an expert Technical Writer and Open Source Maintainer.

Your task is to create a professional, comprehensive README.md file by combining 
analyses from multiple specialized agents.

README Structure Guidelines:
1. Start with a catchy title and badges (if applicable)
2. One-line description
3. Key features as bullet points
4. Tech stack in a clean table or list
5. Architecture overview with diagrams
6. Installation and setup instructions
7. Usage examples
8. API documentation (if applicable)
9. Contributing guidelines
10. License

Writing Style:
- Clear, concise, and professional
- Use proper Markdown formatting
- Include code blocks with syntax highlighting
- Add helpful emojis sparingly for visual appeal
- Ensure all sections flow logically

Important:
- Only document what is actually in the codebase
- Don't invent features that don't exist
- Keep setup instructions accurate and testable
- Include all diagrams provided by agents"""

    def generate_readme(
        self,
        repo_info: Dict[str, Any],
        agent_outputs: Dict[str, Dict[str, Any]]
    ) -> str:
        """
        Generate the final README from all agent outputs.

        Args:
            repo_info: Repository metadata (owner, repo, languages, topics, etc.)
            agent_outputs: Dict mapping cluster names to their analysis results

        Returns:
            Complete README.md content
        """
        # Build the prompt with all analyses
        prompt = self._build_aggregation_prompt(repo_info, agent_outputs)

        messages = [
            SystemMessage(content=self.get_system_prompt()),
            HumanMessage(content=prompt)
        ]

        response = self.model.invoke(messages)

        return self._clean_readme(response.content)

    def _build_aggregation_prompt(
        self,
        repo_info: Dict[str, Any],
        agent_outputs: Dict[str, Dict[str, Any]]
    ) -> str:
        """Build the aggregation prompt with all data."""

        owner = repo_info.get("owner", "")
        repo = repo_info.get("repo", "")
        languages = repo_info.get("languages", {})
        topics = repo_info.get("topics", [])
        dependencies = repo_info.get("dependencies", [])
        project_context = repo_info.get("project_context", {})
        rendered_diagrams = repo_info.get("rendered_diagrams", {})
        folder_structure = repo_info.get("folder_structure", "")

        # Format languages
        lang_str = ", ".join(
            [f"{lang} ({bytes}B)" for lang, bytes in languages.items()][:5])

        # Project context section
        context_str = ""
        if project_context.get("repo_description"):
            context_str += f"- **Description:** {project_context['repo_description']}\n"
        if project_context.get("readme"):
            context_str += f"\n### Existing README Content (for reference):\n```\n{project_context['readme'][:4000]}\n```\n"

        # Format agent analyses
        analyses_str = ""
        diagrams = []
        diagram_images = []
        all_features = []
        all_setup_steps = []
        all_technologies = []

        for cluster_name, analysis in agent_outputs.items():
            if not analysis or analysis.get("summary", "").startswith("No "):
                continue

            analyses_str += f"""
### {cluster_name} Analysis
**Summary:** {analysis.get('summary', 'N/A')}

**Key Files:**
{self._format_list(analysis.get('key_files', []))}

**Technologies:** {', '.join(analysis.get('technologies', [])) or 'N/A'}

**Architecture:** {analysis.get('architecture', 'N/A')}

**Features:**
{self._format_list(analysis.get('features', []))}

**Setup Steps:**
{self._format_list(analysis.get('setup_steps', []))}

---
"""
            # Collect diagrams (mermaid code for fallback)
            if analysis.get('diagrams'):
                diagrams.append(f"#### {cluster_name}\n{analysis['diagrams']}")

            # Collect features
            all_features.extend(analysis.get('features', []))
            all_setup_steps.extend(analysis.get('setup_steps', []))
            all_technologies.extend(analysis.get('technologies', []))

        # Unique technologies
        all_technologies = list(set(all_technologies))

        # Build diagram image references
        if rendered_diagrams:
            for diagram_key, diagram_info in rendered_diagrams.items():
                cluster = diagram_info.get("cluster", "")
                path = diagram_info.get("path", "")
                diagram_images.append(
                    f"- **{cluster}**: `![{cluster} Diagram]({path})`")

        diagrams_images_str = "\n".join(
            diagram_images) if diagram_images else "No diagram images available"

        # Combine mermaid code diagrams for reference
        diagrams_str = "\n\n".join(
            diagrams) if diagrams else "No diagrams available"

        # Format folder structure
        folder_structure_str = f"```\n{folder_structure}\n```" if folder_structure else "Not available"

        return f"""
# Repository Information
- **Owner/Repo:** {owner}/{repo}
- **URL:** https://github.com/{owner}/{repo}
- **Languages:** {lang_str}
- **Topics:** {', '.join(topics) if topics else 'None'}
- **Dependencies:** {', '.join(dependencies[:20]) if dependencies else 'None'}
{context_str}

# Folder Structure
{folder_structure_str}

# Agent Analyses
{analyses_str}

# Rendered Diagram Images (USE THESE IN README!)
{diagrams_images_str}

# Mermaid Diagrams (raw code for reference)
{diagrams_str}

# All Technologies Found
{', '.join(all_technologies) if all_technologies else 'None'}

---

## Your Task

Create a comprehensive README.md that:

1. **Title & Description**: Create an engaging title with the repo name and a clear description

2. **Features**: Combine and deduplicate features from all analyses into a clean list

3. **Tech Stack**: Create a technology table/list from all technologies found

4. **Architecture**: Write an architecture section combining insights from all analyses.
   **IMPORTANT**: If there are rendered diagram images above, use them in the README like this:
   ```
   ![Architecture Diagram](diagrams/ai_engineer_diagram_1.png)
   ```
   Place diagrams in the Architecture section or other relevant sections.

5. **Getting Started**:
   - Prerequisites
   - Installation steps (combine from all analyses)
   - Environment setup
   - Running the project

6. **Project Structure**: Include the folder structure tree provided above in a code block. 
   Add brief descriptions of key directories/files based on insights from the agent analyses.

7. **Usage**: How to use the main features

8. **API** (if Backend cluster exists): Document key endpoints

9. **Contributing**: Standard contributing guidelines

10. **License**: Placeholder for license

Output ONLY the README.md content in proper Markdown format.
"""

    def _format_list(self, items: List[Any]) -> str:
        """Format a list as markdown bullet points."""
        if not items:
            return "- N/A"

        lines = []
        for item in items[:10]:  # Limit to 10 items
            if isinstance(item, dict):
                lines.append(
                    f"- {item.get('path', item.get('name', str(item)))}")
            else:
                lines.append(f"- {item}")
        return "\n".join(lines)

    def _clean_readme(self, content: str) -> str:
        """Clean up the readme content."""
        # Remove any leading/trailing code blocks
        content = content.strip()

        if content.startswith("```markdown"):
            content = content[11:]
        elif content.startswith("```md"):
            content = content[5:]
        elif content.startswith("```"):
            content = content[3:]

        if content.endswith("```"):
            content = content[:-3]

        return content.strip()
