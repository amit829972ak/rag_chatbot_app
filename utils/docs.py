import streamlit as st
import os
from utils.vector_store import update_index_from_file

UPLOAD_DIR = "uploaded_docs"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def handle_upload():
    file = st.sidebar.file_uploader("Upload Document", type=["pdf", "txt", "docx"])
    if file:
        filepath = os.path.join(UPLOAD_DIR, file.name)
        with open(filepath, "wb") as f:
            f.write(file.read())
        update_index_from_file(filepath)
        st.sidebar.success(f"{file.name} uploaded and indexed!")

def handle_delete():
    files = os.listdir(UPLOAD_DIR)
    if files:
        selected = st.sidebar.selectbox("Delete Document", files)
        if st.sidebar.button("Delete"):
            os.remove(os.path.join(UPLOAD_DIR, selected))
            st.sidebar.success(f"{selected} deleted")
