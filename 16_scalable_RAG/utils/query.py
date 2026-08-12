from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from helpers.EmbeddingModel import HugginFaceEmbeddingModel
from helpers.Client import GroqClient
from openai import OpenAI
from openai.resources.chat.completions.completions import  ChatCompletion
from helpers.getEnv import get_env_variable
print("lib loaded")

client:OpenAI = GroqClient().client

#embedding model
hugginFaceEmbeddingModel = HugginFaceEmbeddingModel()

#embedding model
model = hugginFaceEmbeddingModel.embeddingModel


#vector db
# qdraclient 
qclient = QdrantClient(url=get_env_variable("QC_URL"))
#vector db load
print("db loaded")


async def get_response(query:str):

    print("query received : ", query)

    #getting chunks
    #dimention = 768-dimensional
    result = QdrantVectorStore(
      client=qclient,
      collection_name="python-learning",
      embedding=model
    ).similarity_search(
      query=query
    )

    print("context retrieved done");

    SYSTEM_PROMPT = f"""
      You are AI assitent. Solve query using following context only.

      context : {
        result
      }

    """

    #groq loaded
    res:ChatCompletion  =  client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
          {
            "role":"system",
            "content" : SYSTEM_PROMPT
          },
          {
            "role":"user",
            "content" : query
          }
        ]
      )

    print("response generated done");

    return res.choices[0].message.content