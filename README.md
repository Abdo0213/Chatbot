# 🤖 RAG-based Chatbot (CV Assistant)

This project is a Retrieval-Augmented Generation (RAG) chatbot built using FastAPI for the backend and Streamlit for the frontend.

The chatbot can read and process resumes (CVs), store embeddings in a Chroma vector database, and answer user queries in a conversational way with memory.

## ✨ Features

- 📄 Resume Processing: Extracts and splits CVs into chunks for better retrieval.

- 🔎 RAG Pipeline: Retrieves relevant chunks from a vector DB to provide context-based answers.

- 🧠 Conversation Memory: Uses ConversationBufferWindowMemory for contextual dialogue.

- ⚡ LangChain Integration: Handles embedding, chunking, and prompting logic.

- 🧩 Models Used:

  - GoogleGenerativeAIEmbeddings → for embeddings

  - ChatGoogleGenerativeAI → for text generation

- 🗂 Chroma Vector DB → for efficient similarity search.

- 🎨 Streamlit Frontend with a modern UI.

- 🚀 FastAPI Backend with REST endpoints.

## 📦 Installation

1- Clone the repository:

  - git clone https://github.com/yourusername/rag-chatbot.git
  - cd rag-chatbot


2- Create a virtual environment (recommended):

  - python -m venv venv
  - source venv/bin/activate  # Mac/Linux
  - venv\Scripts\activate     # Windows


3- Install dependencies:

  - pip install -r requirements.txt


Or manually:

  - pip install streamlit fastapi pydantic langchain langchain-community langchain-google-genai pypdf chromadb python-dotenv uvicorn

## 🔑 Environment Variables

Create a .env file in the root directory and add:

## Only required for test files
TOGETHER_API_KEY=your_together_api_key

COHERE_API_KEY=your_cohere_api_key

## Required for the chatbot
GOOGLE_API_KEY=your_google_api_key

## ▶️ Running the Application
1️⃣ Start the Backend

  - Navigate to the backend folder and run:
  
  - uvicorn rag:app --reload
  
  
(replace rag with rag2 if you’re using rag2.py)

2️⃣ Start the Frontend

  - In another terminal, navigate to the front folder and run:

  - streamlit run app.py

3️⃣ Access the App

  - Open the provided URL (default: http://localhost:8501) in your browser.

## 🖼 Project Structure
```
rag-chatbot/
│
├── backend/               # FastAPI server code
│   ├── __init__.py
│   ├── rag.py             # Main RAG endpoint
│   ├── rag2.py            # Experimental version
│   └── .env               # API keys (gitignored)
│
├── front/                 # Streamlit interface
│   ├── app.py             # Main UI application
│
├── test.py                
├── main.py                
├── requirements.txt       # Production dependencies
└── README.md              # Project documentation
```

## 📚 Tech Stack

  - Frontend: Streamlit
  
  - Backend: FastAPI
  
  - Database: ChromaDB
  
  - Embeddings: Google Generative AI
  
  - LLM: ChatGoogleGenerativeAI
  
  - Memory: ConversationBufferWindowMemory
## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you’d like to improve.
