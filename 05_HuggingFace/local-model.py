from transformers import pipeline

generator = pipeline(
    "text-generation",
    model="sshleifer/tiny-gpt2"
)

result = generator(
    "this is just timepass",
    max_new_tokens=30
)

print(result[0]["generated_text"])