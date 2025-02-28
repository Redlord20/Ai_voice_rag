from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.document_loaders import PDFPlumberLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
import os
import warnings

warnings.simplefilter("ignore", category=UserWarning)


# Set up FastAPI
app = FastAPI()


# Define allowed origins (You can use ["*"] to allow all origins, but it's not recommended for production)
origins = [
    "http://localhost:3000",  # Allow frontend running on localhost (React, Next.js, etc.)
    #"https://yourdomain.com",  # Add your production frontend domain here
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allows specified origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

@app.get("/")
def read_root():
    return {"message": "CORS enabled!"}


# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Load PDF and process text
pdf_path = "CRLS-FINALBOOK-2023.pdf"
loader = PDFPlumberLoader(pdf_path)
documents = loader.load()


# Split text into chunks for embeddings
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
docs = text_splitter.split_documents(documents)

# Create embeddings and store them in FAISS
embeddings = OpenAIEmbeddings()
vector_store = FAISS.from_documents(docs, embeddings)
retriever = vector_store.as_retriever(search_type="mmr", search_kwargs={"k": 5, "fetch_k": 10})

# Initialize conversational memory
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# Create the ConversationalRetrievalChain
llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.7)
rag_chain = ConversationalRetrievalChain.from_llm(llm, retriever=retriever, memory=memory)

# Define API request body
class QueryRequest(BaseModel):
    question: str

# API Endpoint for querying RAG model
@app.post("/query")
async def query_rag(request: QueryRequest):
    try:
        response = rag_chain.invoke({"question": request.question})
        return {"answer": response["answer"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Run with: uvicorn filename:app --reload
