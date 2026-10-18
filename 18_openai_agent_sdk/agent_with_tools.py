from agents import Agent, Runner, WebSearchTool
from .custom_model import CustomModel

agent = Agent(
    name="Assistant",
    instructions="You are a helpful assistant",
    model=CustomModel().model,
    tools=[WebSearchTool()], #hosted tool
)

result = Runner.run_sync(agent, "give me current weather of surat 394130")
print(result.final_output)

#Disclamer :- 
# with current custom model and provider Hosted tool is not work, it only works with OpenAi models and provider
#kinda disappoitment :)