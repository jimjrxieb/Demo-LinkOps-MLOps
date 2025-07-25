from demo_db.db import init_db
from fastapi import FastAPI, File, HTTPException, UploadFile
from ml_creator.api.agent_generator import generate_agent
from ml_creator.api.model_generator import generate_model
from pydantic import BaseModel

app = FastAPI()


class ModelRequest(BaseModel):
    model_name: str
    purpose: str
    algorithm: str


class AgentRequest(BaseModel):
    agent_name: str
    backlog_url: str
    email_to: str


@app.on_event("startup")
async def startup_event():
    init_db()


@app.post("/create_model")
async def create_model(request: ModelRequest, file: UploadFile = File(...)):
    try:
        dataset_path = f"demo-db/ml-models/data/{file.filename}"
        with open(dataset_path, "wb") as f:
            f.write(await file.read())
        result = generate_model(
            model_name=request.model_name,
            purpose=request.purpose,
            algorithm=request.algorithm,
            dataset=dataset_path,
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/create_agent")
async def create_agent(request: AgentRequest):
    try:
        result = generate_agent(
            agent_name=request.agent_name,
            backlog_url=request.backlog_url,
            email_to=request.email_to,
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
