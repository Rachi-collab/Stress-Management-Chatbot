from fastapi import FastAPI
from pydantic import BaseModel
from chat_engine import get_response   # import from chat_engine.py

app = FastAPI()

class ChatRequest(BaseModel):
    session_id: str
    message: str

@app.post("/chat")
def chat(req: ChatRequest):
    try:
        reply = get_response(req.session_id, req.message)
        return {"response": reply}
    except Exception as e:
        error_msg = str(e)
        if "401" in error_msg or "Unauthorized" in error_msg or "Invalid username or password" in error_msg:
            return {"response": "Error: The Hugging Face API key provided is invalid, unauthorized, or has expired. Please check your HUGGINGFACE_API_KEY in the .env file."}
        return {"response": f"Error calling Hugging Face: {error_msg}"}
