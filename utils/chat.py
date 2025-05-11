from utils.vector_store import search_index
from utils.llm import query_model
import json

def handle_chat(query, model_choice, api_key):
    matches = search_index(query)
    if matches:
        context = "\n".join(matches)
        prompt = f"Context:\n{context}\n\nQuestion: {query}"
        return query_model(prompt, model_choice, api_key)
    else:
        with open("faq.json") as f:
            faq = json.load(f)
        for q, a in faq.items():
            if q.lower() in query.lower():
                return f"From FAQ:\n{a}"
        return "Sorry, no relevant document or FAQ entry found."
