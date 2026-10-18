from agents import Agent, Runner
from .custom_model import CustomModel

model = CustomModel().model

agent = Agent(name="Assistant", instructions="You are a cheerful assistant", model=model)

result = Runner.run_sync(agent, "Hey what's app")
print(result.final_output)