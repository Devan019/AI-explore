
from .mem0_client import Mem0Client

from helpers.Client import GroqClient
client  = GroqClient().client


user_id = input(" ### enter user name : ")

while (True):

    # get input
    user_query = input(" > ")

    # memory search
    memory_search = Mem0Client.search(
        query=user_query,
        user_id=user_id
    )

    memories = ""

    if memory_search and "results" in memory_search:
        for mem in memory_search["results"]:
            memories += f"- {mem['memory']}\n"

    SYSTEM_PROMPT = f"""
You are a helpful AI assistant.

Here is relevant past conversation:
{memories}

Use this memory if relevant to answer the user.
"""

    print(f"Memory found : {memories}")

    # call llm
    res = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
              "role" : "system",
              "content" : SYSTEM_PROMPT 
            },
            {
              "role": "user",
              "content": user_query
            }
        ]
    )

    AI_res = res.choices[0].message.content

    print(f"🤖: {AI_res}")

    # add to memeory
    Mem0Client.add(
        messages=[{"role": "user", "content": user_query},
                  {"role": "assistant", "content": AI_res}],
        user_id=user_id
    )
