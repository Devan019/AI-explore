from helpers.Client import GroqClient

#let's go deep dive into parameters

# | Value | Behavior                               |
# | ----- | -------------------------------------- |
# | 0     | deterministic (same output every time) |
# | 0.3   | focused, factual                       |
# | 0.7   | balanced                               |
# | 1     | creative                               |
# | >1    | chaotic / weird                        |

# Q :-  What is caching and How useful it is?


def genericTemp(tmp: int):
  res = GroqClient().client.chat.completions.create(
    model="openai/gpt-oss-20b",
    messages=[
      {
        "role":"user",
        "content" : "What is caching?In very short term"
      }
    ],
    temperature=tmp
  )

  print(f"for temp : {tmp} response is : {res.choices[0].message.content}")

if __name__ == "__main__":
  genericTemp(0) # tmp = 0

  genericTemp(0.3) 

  genericTemp(0.7)

  genericTemp(1)

  genericTemp(1.3)

  genericTemp(2) 

  genericTemp(3) #edege test
  #openai.BadRequestError: Error code: 400 - {'error': {'message': "'temperature' : number must be at most 2", 'type': 'invalid_request_error'}}




# for temp : 0 response is : Caching is a technique that stores copies of data in a temporary, fast-access location (the cache) so that future requests for that data can be served more quickly, reducing latency and load on the original source.


# for temp : 0.3 response is : Caching is a technique that temporarily stores copies of data (or results) so that future requests for the same information can be served faster, reducing latency and load on the original source.


# for temp : 0.7 response is : Caching is storing frequently accessed data in a faster, temporary storage (like memory) so that future requests can be served more quickly.


# for temp : 1 response is : Caching is a technique that stores copies of data or results in a fast-access location so that future requests can be served quickly without recomputing or rereading the original source.


# for temp : 1.3 response is : Caching is storing frequently used data in a faster, easier‑to‑access location (like RAM or a local disk) so future requests can be served quickly instead of recomputing or fetching it from a slower source.



# for temp : 2 response is : **Caching:** Storing frequently accessed data temporarily to speed up future requests.

