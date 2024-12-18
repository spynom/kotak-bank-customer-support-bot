# app.py
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from src.chatbot import chatbot
import secrets
import logging
import time
# Create an instance of FastAPI
def get_logger(log_file="app.log"):
    # Create a logger
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # Create a StreamHandler for console output
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    # Create a FileHandler for saving logs to a file
    fh = logging.FileHandler(log_file)
    fh.setLevel(logging.DEBUG)

    # Create a formatter and set it for both handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    fh.setFormatter(formatter)

    # Add both handlers to the logger
    logger.addHandler(ch)
    logger.addHandler(fh)

    return logger

logger = get_logger()
app = FastAPI()

class Item(BaseModel):
    session_id : Optional[str] = None
    question : str
# Define a basic route
@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

# Define another endpoint
@app.post("/chat")
def chat(item: Item):
    start_time = time.time()
    session_id = secrets.token_urlsafe(10) if item.session_id is None else item.session_id
    query = item.question
    try:
        response = chatbot(query, session_id)
        time_taken = time.time() - start_time

        logger.info(f"Session_id: {session_id} query: {query} response: {response} Time taken: {time_taken}")
        return {"session_id": session_id, "answer": response}

    except Exception as e:
        logger.error(f"Session_id: {session_id} query: {query} error: {e}")
        return {"error": f"{e}"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
