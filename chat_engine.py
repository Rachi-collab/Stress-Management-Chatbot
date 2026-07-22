import os
from dotenv import load_dotenv

from langchain_huggingface import HuggingFaceEndpoint
from langchain_classic.memory import ConversationBufferMemory
from langchain_classic.chains import ConversationChain

# Load .env
load_dotenv()
HF_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
MODEL_ID = os.getenv("MODEL_ID", "meta-llama/Llama-3.1-8B-Instruct")

if not HF_API_KEY:
    raise ValueError("HUGGINGFACE_API_KEY not found.")

llm = HuggingFaceEndpoint(
    repo_id=MODEL_ID,
    huggingfacehub_api_token=HF_API_KEY,
    temperature=0.7,
)

session_memory_map = {}

def get_response(session_id: str, user_query: str) -> str:
    if session_id not in session_memory_map:
        memory = ConversationBufferMemory(return_messages=False)
        session_memory_map[session_id] = ConversationChain(
            llm=llm,
            memory=memory,
            verbose=False
        )

    conversation = session_memory_map[session_id]
    return conversation.predict(input=user_query)
