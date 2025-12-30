#few shot prompting - direct prompt give at system level with examples bcz prompt is not suffcient :)

#via example accuracy will be increase

from helpers.Client import GroqClient
from openai import OpenAI
from openai.resources.chat.completions.completions import  ChatCompletion
import json

client:OpenAI = GroqClient().client


SYSTEM_PROMPT = """Your are language translater.Only u r giving response of translate related queries.If out of query, say Sorry, I am only able to ans of translating questions

Rules:
- Aways give response in JSON formate

Output formate:
{
  "output" : str or None,
  "isTranslateQue": boolean
}

Q: Hey Translate eduction word from english to spanice
A: {
  "output" : "Educación",
  "isTranslateQue": true
}

Q: Explain me 2+2
A: {
  "output" : "Sorry, I am only able to ans of translating questions",
  "isTranslateQue": false
}

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
      "content" : "Translate eduction word from english to japanies"
    },
  ]
)

data = json.loads(res.choices[0].message.content)

print(data, type(data))

