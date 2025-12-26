# api.py
from fastapi import FastAPI
from pydantic import BaseModel
from agent import run_compliance_agent

app = FastAPI(title="GenAI Compliance Agent")

class ReviewRequest(BaseModel):
    system_description: str

@app.post("/review")
async def review_system(req: ReviewRequest):
    result = await run_compliance_agent(req.system_description)
    return {"result": result}