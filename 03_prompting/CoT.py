# chian of thought - A powerful AI prompting technique CoT :)

# steps - START, multiple Plans, output - Let's go 🔥

from helpers.Client import GroqClient, GeminiClient
from openai import OpenAI
from openai.resources.chat.completions.completions import ChatCompletion
import json

client: OpenAI = GroqClient().client


SYSTEM_PROMPT = """

Your are AI Assitent to solve user queries.

Rules:
- You must respond ONLY in the given JSON format
- You must follow steps: START → PLAN → OUTPUT
- PLAN can appear multiple times
- You must give only ONE step per response
- PLAN must be a short reasoning summary
- Do NOT reveal internal chain-of-thought

JSON format:
{
  "step": "START" | "PLAN" | "OUTPUT",
  "content": string
}

Example interaction:

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

"""

message_histroy: list[dict] = []
print("\n\n\n")
user_prompt: str = input("👉🏻 ")
message_histroy.append(
    {
        "role": "system",
        "content": SYSTEM_PROMPT
    },
)

message_histroy.append(
    {
        "role": "user",
        "content": user_prompt
    },
)

while True:
    try:
        res: ChatCompletion = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=message_histroy,
            response_format={
              "type":"json_object"
            }
        )

        data = res.choices[0].message.content
        json_data: dict = json.loads(data)

        message_histroy.append(
            {
                "role": "assistant",
                "content": data
            },
        )

        step = json_data.get("step")
        content = json_data.get("content")

        if step == "START":
            print(f"🔣 {content}")
        if step == "PLAN":
            print(f"🤖 {content}")
        elif step == "OUTPUT":
            print(f"🚀 {content}")
            break

    except Exception as e:
        print(e)




