from fastapi import FastAPI
from pydantic import BaseModel
import ollama

app = FastAPI(title="Local LLM API", description="Chat with local Ollama model")

MODEL_NAME = "qwen3.5:0.8b"


class PromptRequest(BaseModel):
    prompt: str


class PromptResponse(BaseModel):
    model: str
    response: str


@app.post("/chat", response_model=PromptResponse)
async def chat(request: PromptRequest):
    """
    Send a prompt to the local Ollama model and get a response.
    """
    result = ollama.chat(
        model=MODEL_NAME,
        messages=[
            {"role": "user", "content": request.prompt}
        ]
    )

    return PromptResponse(
        model=MODEL_NAME,
        response=result["message"]["content"]
    )


@app.get("/")
async def root():
    return {"message": "Local LLM API is running", "model": MODEL_NAME}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
