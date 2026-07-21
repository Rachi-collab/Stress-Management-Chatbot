import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

from langchain_huggingface import HuggingFaceEndpoint
from langchain_classic.memory import ConversationBufferMemory
from langchain_classic.chains import ConversationChain

# Load .env
load_dotenv()
HF_API_KEY = os.getenv("HUGGINGFACE_API_KEY")

# Initialize FastAPI app
app = FastAPI()

# CORS - allow frontend to talk to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize HuggingFace model
llm = HuggingFaceEndpoint(
    repo_id="meta-llama/Llama-3-8B-Instruct",
    huggingfacehub_api_token=HF_API_KEY,
    temperature=0.7,
)

memory_map = {}

class ChatRequest(BaseModel):
    session_id: str
    message: str

@app.post("/chat")
async def chat_api(req: ChatRequest):
    session_id = req.session_id

    if session_id not in memory_map:
        memory = ConversationBufferMemory(return_messages=True)
        memory_map[session_id] = ConversationChain(
            llm=llm, memory=memory, verbose=False
        )

    chain = memory_map[session_id]
    try:
        response = chain.predict(input=req.message)
        return {"reply": response, "response": response}
    except Exception as e:
        error_msg = str(e)
        if "401" in error_msg or "Unauthorized" in error_msg or "Invalid username or password" in error_msg:
            err_reply = "Error: The Hugging Face API key is invalid, unauthorized, or has expired. Please verify your HUGGINGFACE_API_KEY in the .env file."
        else:
            err_reply = f"Error: {error_msg}"
        return {"reply": err_reply, "response": err_reply}
