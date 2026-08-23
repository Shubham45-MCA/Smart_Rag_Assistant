[ User (Streamlit UI) ] 
       │
       ├──> Uploads PDF ──> [ FastAPI Backend (Render) ] ──> PyPDFLoader & Text Splitter
       │                                                              │
       │                                                    Google Gemini Embeddings
       │                                                              │
       │                                                              ▼
       └──> Asks Query ───> [ FastAPI Backend (Render) ] ──> ChromaDB Vector Store (k=9)
                                                                      │
                                                                      ▼
                                                            Gemini-3.6-flash LLM
                                                                      │
                                                                      ▼
                                                            [ Precise Answer ]

## Architecture & Deployment
This project follows a **decoupled architecture**:
* **Frontend:** Hosted on **Streamlit Cloud** (`app.py`).
* **Backend:** Hosted on **Render** as a FastAPI web service (`backend.py`).

---

## Getting Started Locally

### 1. Clone the Repository
```bash
git clone [https://github.com/Shubham45-MCA/Smart_Rag_Assistant.git](https://github.com/Shubham45-MCA/Smart_Rag_Assistant.git)
cd Smart_Rag_Assistant

2. Install Dependencies
Ensure you have Python installed, then run:
pip install fastapi uvicorn streamlit langchain langchain-community langchain-core langchain-google-genai chromadb pypdf requests

3. Configure API Key
Make sure your Google Gemini API key is configured securely inside your backend or set as an environment variable (GOOGLE_API_KEY).

4. Run the Application
Step A: Start the FastAPI Backend
uvicorn backend:app --reload

Step B: Start the Streamlit Frontend (Open a new terminal window)
streamlit run app.py
