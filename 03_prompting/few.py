#few shot prompting - direct prompt give at system level with examples bcz prompt is not suffcient :)

#via example accuracy will be increase

from helpers.Client import GroqClient
from openai import OpenAI
from openai.resources.chat.completions.completions import  ChatCompletion

client:OpenAI = GroqClient().client


SYSTEM_PROMPT = """Your are language translater.Only u r giving response of translate related queries.If out of query, say Sorry, I am only able to ans of translating questions

Q: Hey Translate eduction word from english to spanice
A: Educación

Q: Explain me 2+2
A: Sorry, I am only able to ans of translating questions

"""

res:ChatCompletion  =  client.chat.completions.create(
  model="openai/gpt-oss-20b",
  messages=[
    {
      "role" : "system",
      "content" : SYSTEM_PROMPT
    },
    {
      "role":"user",
      "content" : "hey can u give me python code which do transalting"
    },
  ]
)
print(res.choices[0].message.content)

