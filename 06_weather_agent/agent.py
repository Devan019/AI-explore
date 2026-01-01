# chian of thought - A powerful AI prompting technique CoT :)

# steps - START, multiple Plans, output - Let's go 🔥

from helpers.Client import GroqClient, GeminiClient
from openai import OpenAI
from openai.resources.chat.completions.completions import ChatCompletion
from pydantic import BaseModel, Field
from typing import Optional
import json
import requests

client: OpenAI = GroqClient().client


# tools

def getWeather(city: str) -> str:
    api = requests.get(f"https://wttr.in/{city.lower()}?format=%c+%t")
    return api.text

# tool mapper


avaliableTools = {
    "getWeather": getWeather
}

#LLM schema

class LLM_SCHEMA(BaseModel):
    step : str = Field(..., description="it is for step ex PLAN, START, TOOL etc")
    content: str = Field(..., description="it is content of AL response")
    input : Optional[str] = Field(None, description="Input of tool")
    tool : Optional[str] = Field(None, description="tools of avaliable tool for extrenal work")
    output : Optional[str] = Field(None, description="output of called tool")  
     
#      JSON format:
# {
#   "step": "START" | "PLAN" | "OUTPUT" | "TOOL" ,
#   "content": string,
#   "input" : string
# }

SYSTEM_PROMPT = """

Your are AI Assitent to solve user queries.

Rules:
- You must respond ONLY in the given JSON format
- You must follow steps: START → PLAN → OUTPUT
- PLAN can appear multiple times
- You must give only ONE step per response
- PLAN must be a short reasoning summary
- Do NOT reveal internal chain-of-thought
- If you need call tooling u can call tool in avaliable tools list
- for every tool has input and output and wait for observe's output

JSON format:
{
  "step": "START" | "PLAN" | "OUTPUT" | "TOOL" ,
  "content": string,
  "input" : string
}

Avaliable tools
- getWeather(city:str) -> str ; means city as input string and it return current weather of that city as output in string format

Examples:

Example 1 :-

START:
{"step":"START","content":"Write a Python function to add two numbers"}

PLAN:
{"step":"PLAN","content":"Understand the problem requirements and expected output."}

PLAN:
{"step":"PLAN","content":"Decide to use a simple Python function with two parameters."}

PLAN:
{"step":"PLAN","content":"Ensure the function returns the sum and uses clean syntax."}

PLAN:
{"step":"PLAN","content":"Keep the implementation minimal and readable."}

OUTPUT:
{"step":"OUTPUT","content":"def add(a, b):\n    return a + b"}

Example 2 :-

START:
{"step":"START","content":"Solve the expression: 8 + 2 x (3 + 5) ÷ 4"}

PLAN:
{"step":"PLAN","content":"Apply BODMAS to determine the correct order of operations."}

PLAN:
{"step":"PLAN","content":"Solve the expression inside the brackets first."}

PLAN:
{"step":"PLAN","content":"Perform multiplication and division from left to right."}

PLAN:
{"step":"PLAN","content":"Complete the remaining addition."}

OUTPUT:
{"step":"OUTPUT","content":"8 + 2 x (3 + 5) ÷ 4 = 12"}


Example 3 :-

START:
{"step":"START","content":"What is current weather of Surat city?"}

PLAN:
{"step":"PLAN","content":"User want to know about current weather of surat"}

PLAN:
{"step":"PLAN","content":"Ohh, i haven't access of current weather data so i need extrenal tool"}

PLAN:
{"step":"PLAN","content":"I check tools list I think use getWeather tool"}

PLAN:
{"step":"TOOL", "input" : "surat", "tool":"getWeather"}

PLAN:
{"step":"OBSERVE", "output" : "surat's weather is 22 C with cloudy", "tool":"getWeather"}

PLAN:
{"step":"PLAN","content":"Great, I get current weather"}

OUTPUT:
{"step":"OUTPUT","content":"Current weather if surat is 22 C"}


"""

#message history

message_histroy: list[dict] = []
while True:
    print("\n\n")

    #user's input
    user_prompt: str = input("👉🏻 ")

    #add system prompt
    message_histroy.append(
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },
    )

    #add user's prompt
    message_histroy.append(
        {
            "role": "user",
            "content": user_prompt
        },
    )

    #CoT
    while True:
        
        try:
            
            #call LLM
            res: ChatCompletion = client.chat.completions.parse(
                model="moonshotai/kimi-k2-instruct-0905",
                messages=message_histroy,
                response_format=LLM_SCHEMA
            )

            #get json data
            data = res.choices[0].message.parsed

            message_histroy.append(
                {
                    "role": "assistant",
                    "content": json.dumps(data.model_dump())
                },
            )

            step = data.step
            content = data.content

            if step == "START":
                print(f"🔣 {content}")
            elif step == "PLAN":
                print(f"🤖 {content}")
            elif step == "TOOL":
                input_data = data.input
                tool = data.tool

                print(f"🔨 Tool called : {tool}")

                tool_response = avaliableTools[tool](input_data)

                message_histroy.append(
                    {
                        "role": "developer",
                        "content": json.dumps({
                            "step": "OBSERVE",
                            "tool": tool,
                            "output": tool_response
                        })
                    }
                )

            elif step == "OUTPUT":
                print(f"🚀 {content}")
                break

        except Exception as e:
            print(e)
            print("i get error")
            break

    message_histroy.clear()