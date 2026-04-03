from langgraph.graph import StateGraph
from typing import Optional, TypedDict
from langgraph.graph import START, END
from langchain.chat_models import init_chat_model
from langgraph.checkpoint.mongodb import MongoDBSaver
from dotenv import load_dotenv
load_dotenv()

#model --> behind the agent
model = init_chat_model(
  model="openai/gpt-oss-20b",
  model_provider="groq"
)

#create a state node
class AgentState(TypedDict):
  query: str
  output: Optional[str]

#defined a node (always input state -> output state)
def agentNode(state: AgentState) -> AgentState:
  state["output"] = model.invoke(
    input=state["query"]
  ).content

  return state



#create agent
#create graph
graph = StateGraph(AgentState)

#create a node
graph.add_node("llm_node",agentNode)

#create edge
graph.add_edge(START, "llm_node")
graph.add_edge("llm_node", END)



#with memory checkpoint (final state)
DB_URI="localhost:27017"
with MongoDBSaver.from_conn_string(DB_URI) as checkpointer:
    graph = graph.compile(checkpointer=checkpointer)

    config = {
        "configurable": {
            "thread_id": "user_name_devan"
        }
    }

    for chunk in graph.stream(
        {"query":  "hi! I'm DevanAI.I am software developer"},
        config,
        stream_mode="values"
    ):
        print(chunk)

    for chunk in graph.stream(
        {"query":  "hey gpt, tell me about DvenaAI"},
        config,
        stream_mode="values"
    ):
        print(chunk)
