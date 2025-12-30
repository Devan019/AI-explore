
from tiktoken import encoding_for_model, Encoding

# build a transfromer
transformer:Encoding = encoding_for_model("gpt-4")

input = "Hey I am Devan, people are called me DevanAI"

# str to token
encode:list[int] = transformer.encode(input)  # [19182, 358, 1097, 6168, 276, 11, 1274, 527, 2663, 757, 6168, 276, 15836]
print(encode)


# token to str
decode:str = transformer.decode(encode)
print(decode)