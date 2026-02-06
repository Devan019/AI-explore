from langchain_community.document_loaders import PyPDFLoader
from helpers.EmbeddingModel import HugginFaceEmbeddingModel
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from pathlib import Path
print("lib loaded")

#embedding model
hugginFaceEmbeddingModel = HugginFaceEmbeddingModel()

#pdf path
file_path = Path(__file__).parent /  "python.pdf"

#pdf loader
loader = PyPDFLoader(file_path)
print("pdf loaded")

#page extract with content
docs = loader.load()
print(len(docs))

#split loader
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
#spliting
chunks = text_splitter.split_documents(docs)

print("chunks done")

#embedding model
model = hugginFaceEmbeddingModel.embeddingModel

# qdraclient 
qclient = QdrantClient(url="http://localhost:6333")
# #vector db load
print("db loaded")

#storing chunks
#dimention = 768-dimensional
QdrantVectorStore(
  client=qclient,
  collection_name="python-learning",
  embedding=model
).add_documents(
  documents=chunks
)
print("store ready")



