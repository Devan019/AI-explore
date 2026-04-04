# 1. Length Control Parameters
# 🔹 max_completion_tokens
# Max tokens in output

# 👉 Important:

# 1 token ≈ 3–4 characters
# 8192 tokens ≈ ~6k words





# 2.Message / Context Parameters
# 🔹 messages

# Structure:

# [
#   {"role": "system", "content": "You are a helpful assistant"},
#   {"role": "user", "content": "Hello"},
#   {"role": "assistant", "content": "Hi!"}
# ]

# Roles:

# system → behavior control
# user → input
# assistant → history











# 3. Advanced Control (VERY IMPORTANT 🔥)
# 🔹 presence_penalty
# Encourages new topics
# Value	Effect
# 0	normal
# >0	more diverse topics
# 🔹 frequency_penalty
# Reduces repetition

# 👉 Example:

# prevents: "very very very good"
# 🔹 logit_bias
# Force or ban specific tokens

# Example:

# logit_bias={"50256": -100}  # ban token










# 4. JSON / Structured Output
# 🔹 response_format / JSON mode
# Forces structured output
# response_format={"type": "json_object"}

# 👉 Use for:

# APIs
# frontend integration
# DB storage
