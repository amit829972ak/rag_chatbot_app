import streamlit as st
from utils.auth import login_form
from utils.docs import handle_upload, handle_delete
from utils.chat import handle_chat

st.set_page_config(page_title="RAG Chatbot", layout="wide")

if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

st.sidebar.title("Admin Panel")

if not st.session_state['authenticated']:
    login_form()
else:
    st.sidebar.success("Logged in ✅")
    if st.sidebar.button("Logout"):
        st.session_state['authenticated'] = False

    handle_upload()
    handle_delete()

st.sidebar.header("AI Model Settings")
model_choice = st.sidebar.selectbox("Select LLM", ["OpenAI GPT", "Google Gemini", "Claude"])
api_key = st.sidebar.text_input("Enter API Key", type="password")
st.session_state["api_key"] = api_key
st.session_state["model_choice"] = model_choice

st.title("Company RAG Chatbot")
query = st.text_input("Ask your question:")
if query:
    response = handle_chat(query, model_choice, api_key)
    st.markdown("**Response:**")
    st.write(response)
