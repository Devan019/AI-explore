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
        "content" : "A juggler can juggle 16 balls. Half of the balls are golf balls, and half of the golf balls are blue. How many blue golf balls are there?"
      }
    ]
  )
  print(res.choices[0].message.content)

