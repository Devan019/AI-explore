from typing import TypedDict, Optional, List, Dict, Annotated
import json
import logging
import operator

from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage

from .utils import tools

# -----------------------------
# Logging Setup
# -----------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)
log = logging.getLogger("README_AGENT")

# -----------------------------
# Agent State
# -----------------------------


class AgentState(TypedDict):
    owner: str
    repo: str
    messages: Annotated[List[BaseMessage], operator.add]
    readme_md: Optional[str]


# -----------------------------
# LLM with Tools
# -----------------------------
log.info("🧠 Initializing LLM...")
model = init_chat_model(
    model="llama-3.3-70b-versatile",
    model_provider="groq",
    temperature=0.2
)

# Bind tools to the model
model_with_tools = model.bind_tools(tools)
log.info("✅ LLM ready with tools bound")


# =====================================================
# AGENT NODE: Call LLM with Tools
# =====================================================
def agent_node(state: AgentState) -> AgentState:
    log.info("🤖 Agent processing...")

    # If no messages yet, create the initial prompt
    if not state.get("messages"):
        initial_prompt = f"""
You are an expert README generator agent. Your task is to analyze a GitHub repository and generate a comprehensive README.md file.

Repository: {state["owner"]}/{state["repo"]}

You have access to these tools:
1. traverse_repo(owner, repo) - Get the repository file/folder structure as JSON
2. build_structure_summary(owner, repo) - Get a summary of directories with their files and subdirs
3. fetch_file_content(owner, repo, path) - Fetch a single file's content
4. fetch_multiple_files(owner, repo, paths_json) - Fetch multiple files at once (paths_json is a JSON array of paths)

WORKFLOW:
1. First, use build_structure_summary to get an overview of the repository structure
2. Based on the structure, identify important files (entry points, configs, core modules)
3. Use fetch_multiple_files to get the contents of important files
4. Once you have enough information, generate the README

When generating the README, include:
- Project Overview (what problem it solves)
- Solution Approach
- Current Features
- Tech Stack (only what's actually used)
- Execution Flow
- Folder Structure
- Setup & Installation
- Limitations
- Future Improvements

Start by getting the repository structure summary.
"""
        state["messages"] = [HumanMessage(content=initial_prompt)]

    response = model_with_tools.invoke(state["messages"])
    log.info(
        f"📨 LLM response received (tool_calls: {len(response.tool_calls) if response.tool_calls else 0})")

    return {"messages": [response]}


# =====================================================
# TOOL NODE: Execute Tools
# =====================================================
tool_node = ToolNode(tools)


# =====================================================
# ROUTER: Decide next step
# =====================================================
def should_continue(state: AgentState) -> str:
    """Determine if we should continue with tools or end."""
    last_message = state["messages"][-1]

    # If there are tool calls, continue to tools
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        log.info("🔧 Routing to tools...")
        return "tools"

    # Otherwise, we're done - extract README
    log.info("✅ Agent finished, extracting README...")
    return "extract"


# =====================================================
# EXTRACT README
# =====================================================
def extract_readme(state: AgentState) -> AgentState:
    """Extract the final README from the last message."""
    last_message = state["messages"][-1]
    content = last_message.content if hasattr(
        last_message, "content") else str(last_message)

    # Clean up the content - remove any markdown code block wrappers if present
    if content.startswith("```markdown"):
        content = content[11:]
    elif content.startswith("```md"):
        content = content[5:]
    elif content.startswith("```"):
        content = content[3:]

    if content.endswith("```"):
        content = content[:-3]

    state["readme_md"] = content.strip()
    log.info("✅ README extracted")

    return {"readme_md": state["readme_md"]}


# =====================================================
# BUILD GRAPH
# =====================================================
log.info("🔗 Building agent graph")

graph = StateGraph(AgentState)

graph.add_node("agent", agent_node)
graph.add_node("tools", tool_node)
graph.add_node("extract", extract_readme)

graph.add_edge(START, "agent")
graph.add_conditional_edges(
    "agent",
    should_continue,
    {
        "tools": "tools",
        "extract": "extract"
    }
)
graph.add_edge("tools", "agent")
graph.add_edge("extract", END)

agent = graph.compile()

log.info("✅ Agent compiled successfully")


# =====================================================
# RUN
# =====================================================
if __name__ == "__main__":
    log.info("🚀 Starting README Generator Agent")

    state: AgentState = {
        "owner": "Devan019",
        "repo": "smartscout",
        "messages": [],
        "readme_md": None
    }

    final = agent.invoke(state)

    with open("README.md", "w", encoding="utf-8") as f:
        f.write(final["readme_md"])

    log.info("🎉 README.md generated successfully")
