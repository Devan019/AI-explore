#zero shot prompting - direct prompt give at system level

from helpers.Client import GroqClient
from openai import OpenAI
from openai.resources.chat.completions.completions import  ChatCompletion

client:OpenAI = GroqClient().client


SYSTEM_PROMPT = "Your are language translater.Only u r giving response of translate related queries.If out of query, say I am Translater"

res:ChatCompletion  =  client.chat.completions.create(
  model="openai/gpt-oss-20b",
  messages=[
    {
      "role" : "system",
      "content" : SYSTEM_PROMPT
    },
    {
      "role":"user",
      "content" : "translate english to spanice of word - Education"
    },
  ]
)
print(res.choices[0].message.content)

