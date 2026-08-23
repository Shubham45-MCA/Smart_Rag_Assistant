import requests
import streamlit as st

# Configure Streamlit page settings
st.set_page_config(
    page_title="Smart Document Assistant", page_icon="📄", layout="centered"
)

# Custom CSS for enhanced UI aesthetics
st.markdown(
    """
    <style>
    .main {
        padding: 2rem;
    }
    .stTextInput > div > div > input {
        border-radius: 8px;
    }
    .stButton > button {
        border-radius: 8px;
        font-weight: 600;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# Header Section
st.title("📄 Smart Document Assistant")
st.markdown(
    "Upload your PDF document and query its contents to retrieve precise, AI-powered answers instantly."
)

# Sidebar for Document Management
st.sidebar.header("Document Management")
uploaded_file = st.sidebar.file_uploader(
    "Upload PDF Document",
    type="pdf",
    help="Select and upload a PDF file for intelligent indexing.",
)

# Main Query Section
st.markdown("### Query Section")
question = st.text_input(
    "Enter your question regarding the document:",
    placeholder="e.g., What are the key qualifications mentioned?",
)

# Execution Button
if st.button("Generate Answer", type="primary"):
  if question:
    with st.spinner("Analyzing document and generating insights..."):
      files = None
      if uploaded_file is not None:
        files = {
            "file": (
                uploaded_file.name,
                uploaded_file.getvalue(),
                "application/pdf",
            )
        }

      payload = {"question": question}

      try:
        response = requests.post(
            "http://127.0.0.1:8000/ask", files=files, data=payload
        )
        if response.status_code == 200:
          st.success("Response:")
          st.markdown(response.json()["answer"])
        else:
          st.error(
              "An internal error occurred on the backend server. Please check"
              " the server logs."
          )
      except requests.exceptions.ConnectionError:
        st.error(
            "Unable to connect to the backend server. Please ensure FastAPI is"
            " running (`uvicorn backend:app`)."
        )
      except Exception as e:
        st.error(f"An unexpected error occurred: {str(e)}")
  else:
    st.warning("Please enter a valid question before proceeding.")