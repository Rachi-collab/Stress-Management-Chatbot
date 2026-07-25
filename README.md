# Peace Talk - Stress Management Chatbot

Peace Talk is a premium, supportive, and confidential mental health companion designed as a College Minor Project. It features a modern, glassmorphic Light/Dark mode web UI, built-in crisis keyword interception, and a **Retrieval-Augmented Generation (RAG)** pipeline to query localized stress-management guides.

---

## 🌟 Features

*   **Empathetic AI Conversationalist**: Powered by `Meta-Llama-3.1-8B-Instruct` via a remote, serverless Hugging Face Inference Router for fast responses.
*   **Retrieval-Augmented Generation (RAG)**: Leverages `LlamaIndex` to read guidelines from local documents (e.g., `data/Stress-management.txt`) and tailors responses to stress management queries.
*   **Built-in Crisis Safety**: Locally intercepts high-risk keywords (e.g., "suicide", "worthless", "hopeless") to immediately stream Govt of India 24/7 helpline resources (`14416`) without hitting the LLM.
*   **SSE (Server-Sent Events) Streaming**: Yields real-time, token-by-token streaming responses to the frontend for a smooth typing indicator effect.
*   **Premium Front-End**: Glassmorphism aesthetic, custom gradient backdrops, fluid transitions, and immediate theme toggle (Light/Dark).

---

## 🏗️ Architecture & AI Engine

The chatbot backend is built on **FastAPI** with a hybrid AI pipeline:

1.  **Local Embeddings**: Uses the `BAAI/bge-small-en-v1.5` embedding model locally via `sentence-transformers`. This embeds the local text files in the `data/` directory. By running embeddings locally, we eliminate dependency on Hugging Face feature-extraction API rate limits.
2.  **OpenAI-Compatible LLM Router**: Interfaces with the Hugging Face Serverless Router (`https://router.huggingface.co/v1`) using LlamaIndex's `OpenAILike` model wrapper.
3.  **Prompt Customization**: Uses LlamaIndex's prompt helper to rewrite the QA templates, instructing Llama to respond in a warm, caring manner as the supportive "Peace Talk AI".

---

## 📂 Project Directory Structure

```text
Peace talk/
│
├── data/
│   └── Stress-management.txt   # Local RAG knowledge base
│
├── chatbot_ui/                 # Frontend client
│   ├── index.html              # HTML structure with theme toggle
│   ├── styles.css              # Custom styling (glassmorphism, variables, dark mode)
│   └── chatbot.js              # SSE client connecting to port 8000
│
├── main.py                     # Main FastAPI streaming backend app
├── crisis.py                   # Crisis keyword lists & safety streams
├── doc_engine.py               # LlamaIndex vector store & query engine (RAG)
├── chat_engine.py              # LangChain chat engine memory exploration
├── requirements.txt            # Python package dependencies
├── .env                        # Environment variables (API Keys - Ignored by Git)
└── .gitignore                  # Git patterns to ignore secrets & main.py
```

---

## ⚙️ Installation & Setup (From Scratch)

### 1. Prerequisites
Ensure you have **Python 3.10+** installed on your system.

### 2. Clone the Repository
```bash
git clone https://github.com/Rachi-collab/Stress-Management-Chatbot.git
cd "Peace talk"
```

### 3. Create a Virtual Environment
```powershell
python -m venv venv
.\venv\Scripts\activate
```

### 4. Install Dependencies
```powershell
pip install -r requirements.txt
```

### 5. Setup Environment Variables
Create a file named `.env` in the root directory (this is already ignored in `.gitignore` to protect your API keys):
```env
HUGGINGFACE_API_KEY=your_huggingface_api_token_here
```

---

## 🚀 Running the Application

### Step 1: Start the FastAPI Backend
From the root directory with the virtual environment activated, run:
```powershell
uvicorn main:app --reload --port 8000
```
The backend server will launch at `http://localhost:8000`. You can visit `http://localhost:8000/` in your browser to verify it is running (it should return `{"message": "Backend is running!"}`).

### Step 2: Run the Web Frontend
You can launch the frontend client in two ways:
*   **Option A (Simple)**: Double-click `chatbot_ui/index.html` to open it directly in your web browser.
*   **Option B (Recommended)**: Serve it locally using Python's built-in static server to avoid any local file path limitations:
    ```powershell
    python -m http.server 3000 --directory chatbot_ui
    ```
    Open `http://localhost:3000` in your web browser.

---

## 🧪 Testing & Verification

We have created several validation scripts in the scratch directory to verify the streaming logic and RAG retrieval pipeline without running the server:

*   **Test Stream API**:
    ```powershell
    python -u .gemini/antigravity-ide/scratch/verify_streaming.py
    ```
    This prints the SSE stream response in real-time for regular questions and verifies the local crisis safety intercept.

*   **Test Document Retrieve**:
    ```powershell
    python -u .gemini/antigravity-ide/scratch/verify_doc_engine.py
    ```
    This verifies that the local embedding model `BAAI/bge-small-en-v1.5` embeds and queries `data/Stress-management.txt` correctly.