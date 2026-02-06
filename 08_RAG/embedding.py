from helpers.EmbeddingModel import HugginFaceEmbeddingModel
print("embeggig loaded")

hugginFaceEmbeddingModel = HugginFaceEmbeddingModel()

model = hugginFaceEmbeddingModel.embeddingModel
print("model loaded")
embedding = model.embed_query("hey bro ")
print(embedding)