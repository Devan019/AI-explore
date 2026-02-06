#states
from typing import Optional, TypedDict
from langgraph.graph import START, END
from langgraph.graph import StateGraph
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
load_dotenv()

print("Loading model...")
model = init_chat_model(
  model="openai/gpt-oss-20b",
  model_provider="groq"
)
print("Model loaded.")

#1. defined state
class AgentState(TypedDict):
  query: str
  output: Optional[str]

#2. defined nodes
def GPTNode(state: AgentState) -> AgentState:
  state['output'] = model.invoke(state['query']).content
  return state

#3. create agent builder
graph = StateGraph(AgentState)

#4. add nodes to graph
graph.add_node("gpt", GPTNode)

#5. add edges to graph
graph.add_edge(START, "gpt")
graph.add_edge("gpt", END)

#6. compile agent
initial_state = AgentState(query="What is the capital of France?", output=None)
agent = graph.compile()

#7. invoke the agent with the initial state
final_state = agent.invoke(initial_state)

print(final_state)
