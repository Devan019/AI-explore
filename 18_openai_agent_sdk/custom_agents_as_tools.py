import asyncio

from agents import Agent, Runner
from .custom_model import CustomModel

model = CustomModel().model

spanish_agent = Agent(
    name="Spanish agent",
    instructions="You translate the user's message to Spanish",
    model=model
)

french_agent = Agent(
    name="French agent",
    instructions="You translate the user's message to French",
    model=model
)

orchestrator_agent = Agent(
    name="orchestrator_agent",
    instructions=(
        "You are a translation agent. You use the tools given to you to translate. "
        "If asked for multiple translations, you call the relevant tools."
    ),
    tools=[
        spanish_agent.as_tool(
            tool_name="translate_to_spanish",
            tool_description="Translate the user's message to Spanish",
        ),
        french_agent.as_tool(
            tool_name="translate_to_french",
            tool_description="Translate the user's message to French",
        ),
    ],
    model=model
)


async def main():
    result = await Runner.run(orchestrator_agent, input="Say 'Hello, how are you?' in Spanish.")
    print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())