from helpers.Client import GeminiClient
from openai import OpenAI
from openai.resources.chat.completions.completions import  ChatCompletion

client:OpenAI = GeminiClient().client


if __name__ == "__main__":
  res:ChatCompletion  =  client.chat.completions.create(
    model="gemini-2.5-flash",
    messages=[
      {
        "role":"user",
        "content" : "Hey bro!!!, who r u"
      }
    ]
  )
  print(res.choices[0].message.content)

