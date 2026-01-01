from helpers.Client import GroqClient
from openai import OpenAI
from openai.resources.chat.completions.completions import  ChatCompletion

client:OpenAI = GroqClient().client


if __name__ == "__main__":
  res:ChatCompletion  =  client.chat.completions.create(
    model="openai/gpt-oss-20b",
    messages=[
      {
        "role":"user",
        "content" : "current weather of surat?"
      }
    ]
  )
  print(res.choices[0].message.content)

