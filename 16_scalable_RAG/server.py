from fastapi import FastAPI
from Queue.queue import RAGQueue
from bullmq import Job


#fastapi server
app = FastAPI()

#post request - to add job, query
@app.post("/query")
async def add_job(query: str):
    #add job to queue
    job = await RAGQueue.add("RAGQueue", {"query": query})
    return {"job_id": job.id, "status": "Job added to queue"}

#get request - to get job status and result
@app.get("/query/{job_id}")
async def get_job_status(job_id: str):
    job = await Job.fromId(RAGQueue, job_id)
    if job is None:
        return {"error": "Job not found"}
    result = job.returnvalue
    state = await job.getState()
    print("result : ", result, state)
    return {"result": result}


#start app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0/0", port=8000)

