from dotenv import load_dotenv
import os
from mem0 import Memory

load_dotenv()


config = {
    "graph_store": {   #graphdb
        "provider": "neo4j",
        "config": {
            "url": os.getenv("NEO4J_URI"),
            "username": os.getenv("NEO4J_USERNAME"),
            "password": os.getenv("NEO4J_PASSWORD"),
            "database": os.getenv("NEO4J_DATABASE"),
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
