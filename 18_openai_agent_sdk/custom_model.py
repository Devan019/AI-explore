from agents import AsyncOpenAI, OpenAIChatCompletionsModel, set_tracing_disabled
from helpers.Client import GroqClient

set_tracing_disabled(disabled=True)

class CustomModel:
  def __init__(self):
    self.__groqClient = GroqClient().client
    self.__client = AsyncOpenAI(api_key=self.__groqClient.api_key, base_url=self.__groqClient.base_url)
    self.__model = OpenAIChatCompletionsModel(model="openai/gpt-oss-120b", openai_client=self.__client)

  @property
  def model(self):
    return self.__model

CustomModel()