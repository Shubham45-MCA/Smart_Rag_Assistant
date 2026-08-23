# 📄 Smart Document Assistant (RAG)

An enterprise-grade Retrieval-Augmented Generation (RAG) web application engineered with **FastAPI**, **Streamlit**, **LangChain**, and the **Google Gemini API**. This system allows users to upload PDF documents, index them into a persistent vector database, and query their contents to retrieve precise, context-aware answers instantly.

---

## 🏗️ Architecture & Workflow

```text
[ User (Streamlit UI) ] 
       │
       ├──> Uploads PDF ──> [ FastAPI Backend ] ──> PyPDFLoader & Text Splitter
       │                                                      │
       │                                            Google Gemini Embeddings
       │                                                      │
       │                                                      ▼
       └──> Asks Query ───> [ FastAPI Backend ] ──> ChromaDB Vector Store (k=9)
                                                              │
                                                              ▼
                                                    Gemini-3.6-flash LLM
                                                              │
                                                              ▼
                                                    [ Precise Answer ]
1. Clone the Repository
git clone [https://github.com/Shubham45-MCA/Smart_Rag_Assistant.git](https://github.com/Shubham45-MCA/Smart_Rag_Assistant.git)
cd Smart_Rag_Assistant

2. Install Dependencies
Ensure you have Python installed, then run:
pip install fastapi uvicorn streamlit langchain langchain-community langchain-core langchain-google-genai chromadb pypdf requests

3. Configure API Key
Make sure your Google Gemini API key is configured securely inside backend.py.

4. Run the Application
Start the FastAPI Backend:
uvicorn backend:app --reload

Start the Streamlit Frontend (Open a new terminal window):
streamlit run app.py
