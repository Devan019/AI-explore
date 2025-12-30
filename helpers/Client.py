from dotenv import load_dotenv
from openai import OpenAI
import os

class GeminiClient():

  def __init__(self):
    load_dotenv()
    self._client = OpenAI(
      api_key=  os.getenv("GEMINI_API_KEY"),
      base_url= os.getenv("GEMINI_BASE_URL")
    )

  @property
  def client(self):
    return self._client



class GroqClient():
  def __init__(self):
    load_dotenv()
    self._client = OpenAI(
      api_key=  os.getenv("GROQ_API_KEY"),
      base_url= os.getenv("GROQ_BASE_URL")
    )

  @property
  def client(self):
    return self._client
