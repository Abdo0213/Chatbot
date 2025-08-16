from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader
import zipfile
import os
from dotenv import load_dotenv

load_dotenv()

# 1. Load documents
zip_path = "../CVs_1page.zip"
extract_to = "/content/cv"

# Unzip
with zipfile.ZipFile(zip_path, 'r') as zip_ref:
    zip_ref.extractall(extract_to)

def load_pdfs_as_dicts(folder_path):
    documents = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".pdf"):
            loader = PyPDFLoader(os.path.join(folder_path, filename))
            documents.append(loader.load())
    return documents


folder_path = "/content/cv"
docs = load_pdfs_as_dicts(folder_path)

# 2. Split into chunks
splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
chunked_documents = []

for doc in docs:
    chunks = splitter.split_documents(doc)
    for i, chunk in enumerate(chunks):
        chunked_documents.append(chunk)
print(f"Split documents into {len(chunked_documents)} chunks")

# 3. Embeddings
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001",google_api_key=os.getenv("GOOGLE_API_KEY"))

# 4. Create and persist vectorstore
vectorstore = Chroma.from_documents(chunked_documents, embeddings, persist_directory="./chroma_db")
vectorstore.persist()
print("✅ Vectorstore built and saved.")
