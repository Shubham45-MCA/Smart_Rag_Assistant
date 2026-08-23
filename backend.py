import os
from fastapi import FastAPI, UploadFile, File, Form
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# Initialize FastAPI application
app = FastAPI(title="Smart RAG Assistant API", version="1.0")

# 🔑 Configure Gemini API Key
os.environ["GOOGLE_API_KEY"] = os.environ.get("GOOGLE_API_KEY", "Enter Your API Key Here.")

PERSIST_DIR = "./chroma_db"
embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")


@app.post("/ask")
async def ask_question(
    file: UploadFile = File(None), question: str = Form(...)
):
  """Endpoint to process uploaded PDF documents or query the existing vector database."""

  # 1. Process new uploaded file if provided
  if file is not None:
    file_path = f"temp_{file.filename}"
    with open(file_path, "wb") as buffer:
      buffer.write(await file.read())

    loader = PyPDFLoader(file_path)
    docs = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, chunk_overlap=200
    )
    chunks = text_splitter.split_documents(docs)

    vector_store = Chroma.from_documents(
        chunks, embeddings, persist_directory=PERSIST_DIR
    )
    os.remove(file_path)
  else:
    # Load existing persistent database if available
    if os.path.exists(PERSIST_DIR):
      vector_store = Chroma(
          persist_directory=PERSIST_DIR, embedding_function=embeddings
      )
    else:
      return {"answer": "Please upload a PDF file first."}

  # 2. Setup Retriever and LLM components
  retriever = vector_store.as_retriever(search_kwargs={"k": 9})
  llm = ChatGoogleGenerativeAI(model="gemini-3.6-flash", temperature=0.2)

  # 3. Define Modern LCEL Prompt and RAG Chain Pipeline
  template = """You are a helpful AI assistant. Use the provided context to answer the user's question accurately. If the answer is not present in the context, state that you do not have the information.

Context:
{context}

Question: {question}
Answer:"""

  prompt = ChatPromptTemplate.from_template(template)

  def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

  rag_chain = (
      {
          "context": retriever | format_docs,
          "question": RunnablePassthrough(),
      }
      | prompt
      | llm
      | StrOutputParser()
  )

  # 4. Execute execution chain and return response
  response = rag_chain.invoke(question)
  return {"answer": response}