from sentence_transformers import SentenceTransformer
import faiss
import os
import pickle
import fitz  # PyMuPDF
from docx import Document

EMBED_MODEL = SentenceTransformer("all-MiniLM-L6-v2")
INDEX_FILE = "faiss_index.pkl"
DOCS_FILE = "doc_texts.pkl"

def load_index():
    if os.path.exists(INDEX_FILE) and os.path.exists(DOCS_FILE):
        with open(INDEX_FILE, "rb") as f:
            index = pickle.load(f)
        with open(DOCS_FILE, "rb") as f:
            docs = pickle.load(f)
        return index, docs
    return None, []

def save_index(index, docs):
    with open(INDEX_FILE, "wb") as f:
        pickle.dump(index, f)
    with open(DOCS_FILE, "wb") as f:
        pickle.dump(docs, f)

def extract_text(filepath):
    if filepath.endswith(".pdf"):
        doc = fitz.open(filepath)
        return "\n".join(page.get_text() for page in doc)
    elif filepath.endswith(".docx"):
        doc = Document(filepath)
        return "\n".join([p.text for p in doc.paragraphs])
    elif filepath.endswith(".txt"):
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()
    return ""

def update_index_from_file(filepath):
    new_text = extract_text(filepath)
    if not new_text.strip():
        return
    index, docs = load_index()
    all_docs = docs + [new_text]
    embeddings = EMBED_MODEL.encode(all_docs)
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)
    save_index(index, all_docs)

def search_index(query, k=3):
    index, docs = load_index()
    if index is None:
        return []
    q_embed = EMBED_MODEL.encode([query])
    D, I = index.search(q_embed, k)
    return [docs[i] for i in I[0]]
