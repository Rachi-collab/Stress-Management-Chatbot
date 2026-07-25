import os
from dotenv import load_dotenv

from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.llms.huggingface import HuggingFaceLLM

# Load .env
load_dotenv()
HF_API_KEY = os.getenv("HUGGINGFACE_API_KEY")

if not HF_API_KEY:
    raise ValueError("HUGGINGFACE_API_KEY not found. Please check your .env file.")

# Initialize HuggingFace LLM for LlamaIndex
llm = HuggingFaceLLM(
    model_name="meta-llama/Llama-3.1-8B-Instruct",   # HF model
    tokenizer_name="meta-llama/Llama-3.1-8B-Instruct",
    context_window=4096,
    max_new_tokens=512,
    temperature=0.7,
    api_key=HF_API_KEY
)

# Load documents from the 'data' directory
documents = SimpleDirectoryReader('data').load_data()

# Create vector index
index = VectorStoreIndex.from_documents(documents)

# Create query engine
query_engine = index.as_query_engine(llm=llm)

# Query function
def query_documents(user_query: str) -> str:
    response = query_engine.query(user_query)
    return str(response)
