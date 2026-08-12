import asyncio
import logging
from bullmq import Worker
from ..utils.query import get_response


async def process(job, token):
    query_text = job.data.get("query", "")
    
    data = await get_response(query_text)
    return data

async def main():
    worker = Worker(
        "RAGQueue",
        process,
        {
            "connection": {
                "host": "localhost",
                "port": 6380,
            },
            "concurrency": 5,
        }
    )
    
    try:
        # Keep the main loop running
        await asyncio.Event().wait()
    except asyncio.CancelledError:
        pass
    finally:
        await worker.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Worker stopped by user.")
