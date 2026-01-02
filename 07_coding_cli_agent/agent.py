# chian of thought - A powerful AI prompting technique CoT :)

# steps - START, multiple Plans, output - Let's go 🔥

from helpers.Client import GroqClient, GeminiClient
from openai import OpenAI
from openai.resources.chat.completions.completions import ChatCompletion
from pydantic import BaseModel, Field
from typing import Optional
import json
import requests
import os
from pathlib import Path

client: OpenAI = GroqClient().client


# tools

def mkdir(dir: str) -> str:
    Path(dir).mkdir(parents=True, exist_ok=True)
    return f"created folder {dir}"


def createFile(file: str) -> str:
    Path(file).parent.mkdir(parents=True, exist_ok=True)

    if Path(file).exists():
        return f"file already exists {file}"

    with open(file, "+x", encoding="utf-8") as _:
        pass
    return f"file is created {file}"


def writeFile(file: str, content: str) -> str:
    with open(file, "+w", encoding="utf-8") as f:
        f.write(content)
    return f"content is added"


def readFile(file: str) -> str:
    with open(file, "+r", encoding="utf-8") as f:
        return f.read()
    return f"Not readable"


# tool mapper


avaliableTools = {
    "mkdir": mkdir,
    "createFile": createFile,
    "writeFile": writeFile,
    "readFile": readFile
}

# LLM schema\


class Input_Schema(BaseModel):
    file: Optional[str] = Field(None, description="file name")
    content: Optional[str] = Field(None, description="content of file")


class LLM_SCHEMA(BaseModel):
    step: str = Field(...,
                      description="it is for step ex PLAN, START, TOOL etc")
    content: Optional[str] = Field(...,
                                   description="it is content of AL response")
    input: Optional[str | Input_Schema] = Field(
        None, description="Input of tool")
    tool: Optional[str] = Field(
        None, description="tools of avaliable tool for extrenal work")
    output: Optional[str] = Field(None, description="output of called tool")
    file_content: Optional[str] = Field(None, description="content of file")


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
- mkdir(folder:str) -> str => it is take input as path and create a folder and return a message
- createFile(file:str) -> str => it is take input as path and create a file and return a message
- writeFile(file:str, content) -> str => it is take input as path and content, then add content at that file and return a message
- readFile(file:str) -> str => it is take input as path and return the content of that file


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
{"step":"START","content":"Create a folder named logs and inside it create a file app.log"}

PLAN:
{"step":"PLAN","content":"User wants filesystem operations using CLI-like tools"}

PLAN:
{"step":"PLAN","content":"Creating folder requires mkdir tool"}

TOOL:
{"step":"TOOL","tool":"mkdir","input":"logs"}

OBSERVE:
{"step":"OBSERVE","tool":"mkdir","output":"created folder logs"}

PLAN:
{"step":"PLAN","content":"Folder created successfully, now create file inside it"}

TOOL:
{"step":"TOOL","tool":"createFile","input":"logs/app.log"}

OBSERVE:
{"step":"OBSERVE","tool":"createFile","output":"file is created logs/app.log"}

PLAN:
{"step":"PLAN","content":"Now write initial content to the log file"}

TOOL:
{"step":"TOOL","tool":"writeFile","input":{"file":"logs/app.log","content":"Server started successfully"}}

OBSERVE:
{"step":"OBSERVE","tool":"writeFile","output":"content is added"}

OUTPUT:
{"step":"OUTPUT","content":"Folder logs and file app.log created with initial content"}

"""

# message history

message_histroy: list[dict] = []
while True:
    print("\n\n")

    # user's input
    user_prompt: str = input("👉🏻 ")

    # add system prompt
    message_histroy.append(
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },
    )

    # add user's prompt
    message_histroy.append(
        {
            "role": "user",
            "content": user_prompt
        },
    )

    # CoT
    while True:

        try:

            # call LLM
            res: ChatCompletion = client.chat.completions.parse(
                model="moonshotai/kimi-k2-instruct-0905",
                messages=message_histroy,
                response_format=LLM_SCHEMA
            )

            # get json data
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

                if isinstance(input_data, dict) or isinstance(input_data, Input_Schema):
                    tool_response = avaliableTools[tool](
                        input_data.file,
                        input_data.content
                    )
                else:
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
