from fastapi import FastAPI
from pydantic import BaseModel
from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain.memory import ConversationBufferWindowMemory
from langchain.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
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

@app.post("/ask2")
async def ask(query: Query):
    response = qa_chain.invoke({
        "input": query.question,
        "chat_history": memory.chat_memory.messages  # 👈 manually inject memory
    })
    # Save this exchange into memory
    memory.chat_memory.add_user_message(query.question)
    memory.chat_memory.add_ai_message(response["answer"])
    return {"answer": response["answer"]}
