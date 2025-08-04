from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.services.llm.agent import test_llm

app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def read_root():
    return {"Hello": "World!"}

@app.get("/chat/{message}")
async def chat(message: str):
    response = test_llm(message)
    return {"response": f"You said: {response.content}"}