from agents import Agent, Runner
from agents.decorators import tool
from .custom_model import CustomModel
import requests

@tool(name_override="weather_search")
def getWeather(city: str) -> str:

    """
      this is weather search tool 
      parameter:
      city as str
      respone type : str
    """
    
    api = requests.get(f"https://wttr.in/{city.lower()}?format=%c+%t")
    return api.text


agent = Agent(
    name="Assistant",
    instructions="You are a helpful assistant",
    model=CustomModel().model,
    tools=[getWeather], 
)

result = Runner.run_sync(agent, "give me current weather of surat 394130")
print(result.final_output)
