from fastapi import FastAPI
from pydantic import BaseModel
from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain.memory import ConversationBufferWindowMemory
from langchain.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
from dotenv import load_dotenv
import zipfile
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os

load_dotenv()
app = FastAPI()

embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001",google_api_key=os.getenv("GOOGLE_API_KEY"))

# 1. Load documents
#zip_path_global = "../uploads"
extract_to = "../content/cv"

# Unzip

def unzip(zip_path):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)

def load_pdfs_as_dicts(folder_path):
    documents = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".pdf"):
            loader = PyPDFLoader(os.path.join(folder_path, filename))
            documents.append(loader.load())
    return documents

def split_files(docs):
    # 2. Split into chunks
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunked_documents = []

    for doc in docs:
        chunks = splitter.split_documents(doc)
        for i, chunk in enumerate(chunks):
            chunked_documents.append(chunk)
    return chunked_documents

class File(BaseModel):
    path: str

@app.post("/build")
async def ask(file: File):
    unzip(file.path)
    docs = load_pdfs_as_dicts(extract_to)
    chunked_documents = split_files(docs)
    vectorstore = Chroma.from_documents(chunked_documents, embeddings, persist_directory="./chroma_db")
    vectorstore.persist()


# 1. Load embeddings + vectorstore
#embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001",google_api_key=os.getenv("GOOGLE_API_KEY"))
vectorstore = Chroma(persist_directory="./chroma_db", embedding_function=embeddings)

# 2. Retriever
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

# 3. LLM
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash",google_api_key=os.getenv("GOOGLE_API_KEY"), temperature=0)

# 4. Custom Prompt
system_prompt = (
    "You are an assistant for question-answering tasks. "
    "Use the retrieved context and the past conversation to answer the question. "
    "Keep answers concise (max 3 sentences)."
    "\n\nContext:\n{context}\n\nConversation history:\n{chat_history}"
)

chat_prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("human", "{input}"),
])

# 5. Memory (window to avoid growing too big)
memory = ConversationBufferWindowMemory(
    memory_key="chat_history",
    k=5,  # keep last 5 exchanges
    return_messages=True,
    output_key="answer"
)

# 6. Stuff documents chain (uses our custom prompt)
doc_chain = create_stuff_documents_chain(llm, chat_prompt)

# 7. Retrieval chain (wraps retriever + doc_chain)
qa_chain = create_retrieval_chain(retriever, doc_chain)

# Request schema
class Query(BaseModel):
    question: str

@app.post("/ask")
async def ask(query: Query):
    response = qa_chain.invoke({
        "input": query.question,
        "chat_history": memory.chat_memory.messages  # 👈 manually inject memory
    })
    # Save this exchange into memory
    memory.chat_memory.add_user_message(query.question)
    memory.chat_memory.add_ai_message(response["answer"])
    return {"answer": response["answer"]}
