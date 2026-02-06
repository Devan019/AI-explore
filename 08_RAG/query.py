from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from helpers.EmbeddingModel import HugginFaceEmbeddingModel
from helpers.Client import GroqClient
from openai import OpenAI
from openai.resources.chat.completions.completions import  ChatCompletion

print("lib loaded")

client:OpenAI = GroqClient().client



#embedding model
hugginFaceEmbeddingModel = HugginFaceEmbeddingModel()

#embedding model
model = hugginFaceEmbeddingModel.embeddingModel

#user query 
query = input(" > : ")

#vector db
# qdraclient 
qclient = QdrantClient(url="http://localhost:6333")
#vector db load
print("db loaded")

#getting chunks
#dimention = 768-dimensional
result = QdrantVectorStore(
  client=qclient,
  collection_name="python-learning",
  embedding=model
).similarity_search(
  query=query
)

SYSTEM_PROMPT = f"""
  You are AI assitent. Solve query using following context only.

  context : {
    query
  }

"""

#groq loaded
res:ChatCompletion  =  client.chat.completions.create(
    model="openai/gpt-oss-20b",
    messages=[
      {
        "role":"user",
        "content" : "current weather of surat?"
      }
    ]
  )


#api