from together import Together
from fastapi import FastAPI
from dotenv import load_dotenv
from pydantic import BaseModel
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ConversationBufferMemory
from langchain.chains import LLMChain
from langchain_together import ChatTogether
import os

load_dotenv()

app = FastAPI()

LLM_MODEL = "meta-llama/Llama-3.3-70B-Instruct-Turbo-Free"
api_key = os.getenv("api_key")
client = Together(api_key=api_key)

class Chat_Request(BaseModel):
    user_id: str
    prompt: str

class Chat_Response(BaseModel):
    answer: str

# Create Together AI LLM wrapper
llm = ChatTogether(
    model=LLM_MODEL,
    api_key=api_key,
    temperature=0.7
)

# Create ChatPromptTemplate with system role and message history
prompt_template = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful AI assistant. Answer all questions to the best of your ability."),
    MessagesPlaceholder(variable_name="history"),
    ("user", "{input}")
])

# Memory store per user
user_memories = {}

def get_chain_for_user(user_id: str):
    # Get or create memory for the user
    if user_id not in user_memories:
        user_memories[user_id] = ConversationBufferMemory(
            memory_key="history",
            return_messages=True  # IMPORTANT: ChatPromptTemplate needs messages, not plain text
        )
    memory = user_memories[user_id]

    # Create a chain with memory
    chain = LLMChain(
        llm=llm,
        prompt=prompt_template,
        memory=memory
    )
    return chain

@app.post("/langchain/chat", response_model=Chat_Response)
async def chat_with_history(request: Chat_Request):
    chain = get_chain_for_user(request.user_id)
    result = chain.run(input=request.prompt)
    return Chat_Response(answer=result)

"""
{
    "user_id": "test_user_1",
    "prompt": "Hello, who are you?"
}
{
    "user_id": "test_user_1",
    "prompt": "What did I just ask you?"
}
{
    "user_id": "test_user_2",
    "prompt": "What did I just ask you?"
}

"""

@app.post("/together/chat", response_model=Chat_Response)
async def chat_with_llma(request: Chat_Request):
    response = client.chat.completions.create(
        model=LLM_MODEL,
        messages=[
            {
                "role": "user",
                "content": request.prompt
            }
        ]
    )
    return Chat_Response(answer=response.choices[0].message.content) 

# @app.get("/")
# def read_root():
#     return{"message":"hello world"}

# @app.get("/hello/{name}")
# def read_root(name:str):
#     return{"message":f"hello {name}"}



# class query(BaseModel):
#     userid: str
#     message: str

# @app.post("/chat/")
# def read_root(query:query):
#     return{"message":f"User {query.userid} says: {query.message}"}

