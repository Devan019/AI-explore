from helpers.Client import GroqClient

#let's go deep dive into streaming

# stream
# True → response comes token-by-token (like ChatGPT typing)
# False → full response at once

# Q :-  What is caching and How useful it is?


import time
from helpers.Client import GroqClient

def genericStream(stream: bool):
    res = GroqClient().client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "user",
                "content": "Explain caching in detail with examples"
            }
        ],
        stream=stream
    )

    if stream:
        for chunk in res:
            content = chunk.choices[0].delta.content or ""
            print(content, end="", flush=True)
            time.sleep(0.03) 
        print()
    else:
        print(res.choices[0].message.content)


if __name__ == "__main__":
    genericStream(True)
    print("\n--- NON STREAM ---\n")
    genericStream(False)