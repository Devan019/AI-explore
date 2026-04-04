from dotenv import load_dotenv
import os
from mem0 import Memory

load_dotenv()


config = {
    "vector_store": {  # vector db
        "provider": "qdrant",
        "config": {
            "collection_name": "user_personal",
            "host": "localhost",
            "port": 6333,
            "embedding_model_dims": 384
        }
    },
    "llm": {            #LLM
        "provider": "groq",
        "config": {
            "model" : "openai/gpt-oss-20b",
            "api_key" : os.getenv("GROQ_API_KEY")
        }
    },
    "embedder": {       # embedding model
        "provider": "huggingface",
        "config": {
            "model": "multi-qa-MiniLM-L6-cos-v1",
            "embedding_dims": 384
        }
    }
}

# client
Mem0Client = Memory.from_config(config)
