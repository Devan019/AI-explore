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
        "content" : "Hey bro!!!, who r u"
      }
    ]
  )
  print(res.choices[0].message.content)

