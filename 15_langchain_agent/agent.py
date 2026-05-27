from langchain.agents import create_agent
import time
import os
from langchain_groq import ChatGroq
import dotenv
from .mytool import getWeather

dotenv.load_dotenv()

model = ChatGroq(
    temperature=0,
    model_name="openai/gpt-oss-20b",
    groq_api_key=os.getenv("GROQ_API_KEY")
)


agent = create_agent(
    model,
    tools=[getWeather],
    system_prompt="You are a AI expert to do automate task.",
)


if __name__ == "__main__":
    st = time.time()
    response = agent.invoke(
        {"messages": [{"role": "user", "content": "What is the current weather of New York?"}]}
    )
    end = time.time()
    print(f"Response time: {end - st} seconds")
    print(response["messages"][-1].content)
