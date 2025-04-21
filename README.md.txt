🦙 i4Twins – Llama AI RAG for Industrial Data
A Django‑based system inspired by Google’s LM Notebook, designed to process PDFs and other industrial data using Retrieval‑Augmented Generation (RAG) powered by local Llama models via Ollama. Ask questions in natural language and receive precise, context‑aware answers.

🚀 Key Features
📥 Multi‑Source Data Ingestion
Upload PDFs or enter URLs to ingest industrial documents into the RAG pipeline.

🔍 Retrieval‑Augmented Generation
Combine a vector database (FAISS or Chroma) with Llama LLMs to fetch relevant document chunks.

🧠 Intelligent Q&A API
Send REST requests with your question and receive clean Markdown‑formatted answers.

⚙️ Local LLM Serving
Run everything on your own machine—no cloud dependency—via the Ollama CLI.

📦 Prerequisites
Python 3.8+

Django 4.x

Ollama CLI (for local Llama model serving)

Vector DB: FAISS or Chroma

(Optional) Windows Subsystem for Linux (WSL) on Windows

🛠 Installation
1. Clone the repository
git clone https://github.com/your-username/llama-rag-industrial.git
cd llama-rag-industrial

2. Install Python dependencies
pip install -r requirements.txt

⚙️ Model Setup & Execution
1. Install Ollama
Download and install the Ollama CLI for your OS:
https://ollama.com/download

Verify installation:
ollama version

2. (Windows Only) Enable WSL
If you’re on Windows, enable WSL to ensure full compatibility:

wsl --install
wsl --list --verbose

3. List & Pull a Llama Model
List available remote models:
ollama list-remote

Download your chosen model (e.g., llama3.2-vision:90b):
ollama pull llama3.2-vision:90b

4. Verify Downloaded Models
ollama list

5. Start the Ollama Server
Run the model locally on port 11434 (default):

ollama serve llama3.2-vision:90b --port 11434

Tip: To run in the background on Linux/macOS, append & at the end.

6. (Optional) Set Environment Variables
Point your app to the correct model and host:

export OLLAMA_MODEL="llama3.2-vision:90b"
export OLLAMA_HOST="localhost:11434"

▶️ Launching the Django App
Apply database migrations
python manage.py migrate

Run the development server
python manage.py runserver 8000

Use the UI
Open your browser at http://localhost:8000 to upload PDFs or enter URLs.

Use the REST API
curl -X POST http://localhost:8000/api/query \
-H "Content-Type: application/json" \
-d '{"question":"What is the recommended operating temperature?"}'

📝 Full Quick‑Start Example
Clone + install dependencies
git clone https://github.com/your-username/llama-rag-industrial.git
cd llama-rag-industrial
pip install -r requirements.txt

Install + verify Ollama
ollama version

(Windows) Enable WSL if needed
wsl --install

Download model
ollama pull llama3.2-vision:90b

Serve model locally
ollama serve llama3.2-vision:90b --port 11434 &

Migrate + run Django
python manage.py migrate
python manage.py runserver 8000

📖 Further Reading
Ollama Documentation: https://ollama.com/docs

RAG with Llama Examples: https://github.com/ollama/llama-rag-examples

Django REST Framework: https://www.django-rest-framework.org/
