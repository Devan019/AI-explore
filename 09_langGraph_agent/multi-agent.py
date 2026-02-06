# states
from typing import Optional, TypedDict
from xml.parsers.expat import model
from langgraph.graph import START, END
from langgraph.graph import StateGraph
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
load_dotenv()

print("Loading models...")
planner_model = init_chat_model(
    model="llama-3.3-70b-versatile",
    model_provider="groq"
)

research_model = init_chat_model(
    model="openai/gpt-oss-20b",
    model_provider="groq"
)

writer_model = init_chat_model(
    model="openai/gpt-oss-120b",
    model_provider="groq"
)
print("Models loaded.")

# 1. defined state


class AgentState(TypedDict):
    query: str
    plan: Optional[str]
    research: Optional[str]
    output: Optional[str]

# 2. defined nodes


def PlannerAgent(state: AgentState) -> AgentState:
    response = planner_model.invoke(
        f"Create a short plan to answer: {state['query']}"
    ).content

    print(f"\n\n\nPlanner response: {response}")

    state["plan"] = response
    return state


def ResearchAgent(state: AgentState) -> AgentState:
    response = research_model.invoke(
        f"Using this plan:\n{state['plan']}\n"
        f"Research facts for: {state['query']}"
    ).content

    print(f"\n\n\nResearcher response: {response}")
    state["research"] = response
    return state


def WriterAgent(state: AgentState) -> AgentState:
    response = writer_model.invoke(
        f"Using the research below, write a clear final answer:\n"
        f"{state['research']}"
    ).content

    print(f"\n\n\nWriter response: {response}")
    state["output"] = response
    return state


# 3. create agent builder
graph = StateGraph(AgentState)

# 4. add nodes to graph
graph.add_node("planner", PlannerAgent)
graph.add_node("researcher", ResearchAgent)
graph.add_node("writer", WriterAgent)

# 5. add edges to graph
graph.add_edge(START, "planner")
graph.add_edge("planner", "researcher")
graph.add_edge("researcher", "writer")
graph.add_edge("writer", END)

# 6. compile agent
initial_state = AgentState(
    query="What is 2+5+6+2-24/49+39", output=None)
agent = graph.compile()

# 7. invoke the agent with the initial state
final_state = agent.invoke(initial_state)

print(final_state)
