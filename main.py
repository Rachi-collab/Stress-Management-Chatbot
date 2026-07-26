# main.py
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles
import json
import asyncio
from dotenv import load_dotenv
from crisis import contains_crisis_keywords, SAFETY_MESSAGE
from doc_engine import query_documents_stream

# Load .env
load_dotenv()
HF_API_KEY = os.getenv("HUGGINGFACE_API_KEY")

if not HF_API_KEY:
    raise ValueError("HUGGINGFACE_API_KEY not found. Please check your .env file.")

app = FastAPI()

# Enable CORS for local testing
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/chat")
async def chat(data: dict):
    user_input = data.get("message", "")

    # Check for crisis keywords locally
    if contains_crisis_keywords(user_input):
        async def stream_safety():
            chunk_size = 25
            for i in range(0, len(SAFETY_MESSAGE), chunk_size):
                chunk = SAFETY_MESSAGE[i:i+chunk_size]
                chunk_data = {
                    "choices": [{
                        "delta": {"content": chunk}
                    }]
                }
                yield f"data: {json.dumps(chunk_data)}\n\n"
                await asyncio.sleep(0.01)
            yield "data: [DONE]\n\n"
        return StreamingResponse(stream_safety(), media_type="text/event-stream")

    # RAG Event generator utilizing LlamaIndex querying
    async def event_generator():
        try:
            # Query the RAG engine stream
            response_gen = query_documents_stream(user_input)
            
            for chunk in response_gen:
                if chunk:
                    chunk_data = {
                        "choices": [{
                            "delta": {"content": chunk}
                        }]
                    }
                    yield f"data: {json.dumps(chunk_data)}\n\n"
                    # Small sleep to yield control to the event loop
                    await asyncio.sleep(0.01)
            yield "data: [DONE]\n\n"
        except Exception as e:
            err_msg = f"Error: Failed to connect to Hugging Face: {str(e)}"
            yield f"data: {json.dumps({'choices': [{'delta': {'content': err_msg}}]})}\n\n"
            yield "data: [DONE]\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")

# Mount frontend static files at root (/) so FastAPI serves index.html at the home route
app.mount("/", StaticFiles(directory="chatbot_ui", html=True), name="static")
