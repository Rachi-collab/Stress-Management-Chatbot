import os
from dotenv import load_dotenv
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.llms.openai_like import OpenAILike
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import PromptTemplate

# Load .env using absolute path relative to the workspace directory
load_dotenv()
HF_API_KEY = os.getenv("HUGGINGFACE_API_KEY")

if not HF_API_KEY:
    raise ValueError("HUGGINGFACE_API_KEY not found. Please check your .env file.")

# Initialize Hugging Face LLM via OpenAILike router (which supports META-LLAMA-3.1 on Hugging Face router)
llm = OpenAILike(
    model="meta-llama/Llama-3.1-8B-Instruct",
    api_base="https://router.huggingface.co/v1",
    api_key=HF_API_KEY,
    temperature=0.7,
    is_chat_model=True
)

# Initialize BGE Small English Embedding Model locally
embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")

# Configure LlamaIndex global settings
Settings.llm = llm
Settings.embed_model = embed_model

# Load documents from the 'data' directory
documents = SimpleDirectoryReader('data').load_data()

# Create vector store index
index = VectorStoreIndex.from_documents(documents)

# Create query engine with streaming enabled
query_engine = index.as_query_engine(streaming=True)

# Custom QA prompt to ensure the bot behaves as "Peace Talk AI"
qa_prompt_tmpl_str = (
    "You are Peace Talk AI, a supportive and warm mental health assistant. "
    "Use the following pieces of context to help support the user. If the answer cannot be found in the context, "
    "still respond in a warm and empathetic way, using your general knowledge if appropriate, but prioritize the guidelines if they apply.\n\n"
    "Context information:\n"
    "---------------------\n"
    "{context_str}\n"
    "---------------------\n"
    "User Message: {query_str}\n\n"
    "Empathetic Response: "
)
qa_prompt_tmpl = PromptTemplate(qa_prompt_tmpl_str)
query_engine.update_prompts({"response_synthesizer:text_qa_template": qa_prompt_tmpl})

# Non-streaming query function for backward compatibility
def query_documents(user_query: str) -> str:
    response = query_engine.query(user_query)
    return str(response)

# Streaming query function for main.py
def query_documents_stream(user_query: str):
    response = query_engine.query(user_query)
    return response.response_gen
