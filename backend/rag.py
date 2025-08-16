from fastapi import FastAPI
from pydantic import BaseModel
from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

# 1. Load embeddings + vectorstore
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001",google_api_key=os.getenv("GOOGLE_API_KEY"))
vectorstore = Chroma(persist_directory="./chroma_db", embedding_function=embeddings)

# 2. Retriever
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

# 3. LLM
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash",google_api_key=os.getenv("GOOGLE_API_KEY"), temperature=0)

# 4. Memory
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True, output_key="answer")

# 5. Conversational Chain
qa_chain = ConversationalRetrievalChain.from_llm(
    llm=llm,
    retriever=retriever,
    memory=memory,
    return_source_documents=True,
    output_key="answer"
)

# Request schema
class Query(BaseModel):
    question: str

@app.post("/ask")
async def ask(query: Query):
    response = qa_chain.invoke({"question": query.question})
    return {"answer": response["answer"]}
