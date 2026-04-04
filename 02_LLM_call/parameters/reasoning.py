from helpers.Client import GroqClient

#let's go deep dive into reasoning

# | Value  | Meaning                                         |
# | ------ | ----------------------------------------------- |
# | low    | fast, shallow                                   |
# | medium | balanced                                        |
# | high   | deeper reasoning (slower, better for DSA/logic) |


# Q :-  What is caching and How useful it is?


def genericReason(effort: str):
  res = GroqClient().client.chat.completions.create(
    model="openai/gpt-oss-20b",
    messages=[
      {
        "role":"user",
        "content" : "What is caching?In very short term"
      }
    ],
    reasoning_effort=effort
  )

  print(f"for reason : {effort} response is : {res.choices[0].message.content}")

if __name__ == "__main__":
  genericReason("low") 

  genericReason("medium")

  genericReason("high")



# for reason : low response is : Caching is a technique that stores a copy of data or the result of a computation in a quick‑to‑access location (like memory). When the same data is requested again, the system can return the cached copy instead of recomputing or re‑retrieving it, speeding up response times and reducing load.


# for reason : medium response is : **Caching** is storing copies of data or results in a fast-access location (like memory or local storage) so future requests can be served more quickly without recomputing or re-fetching from slower sources.



# for reason : high response is : Caching is the practice of temporarily storing copies of frequently accessed data in fast, easily reachable storage so that future requests can be served more quickly.