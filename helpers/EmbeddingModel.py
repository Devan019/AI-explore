from langchain_huggingface import HuggingFaceEmbeddings

class HugginFaceEmbeddingModel():
  def __init__(self):
    self._embeddingsModel = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")

  @property
  def embeddingModel(self):
    return self._embeddingsModel