from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from agent_service import agent_query
from todo_service import get_tasks

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Todo Agent API"}


class MessageRequest(BaseModel):
    message: str


@app.post("/agent")
async def agent(request: MessageRequest):
    return await agent_query(request.message)


@app.get("/tasks")
async def tasks():
    return get_tasks()