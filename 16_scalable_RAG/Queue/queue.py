from bullmq import Queue

RAGQueue = Queue(
    "RAGQueue",
    {
        "connection": {
            "host": "localhost",
            "port": 6380,
        }
    }
)
