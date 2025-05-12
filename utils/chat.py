import streamlit as st
from utils.vector_store import search_index, extract_text_from_file
from utils.llm import query_model
import json
import os

def handle_chat(query, model_choice, api_key):
    """
    Handle a chat query using RAG methodology.
    
    Args:
        query: User query string
        model_choice: Selected AI model
        api_key: API key for the selected model
        
    Returns:
        Response string from the AI model
    """
    try:
        # Get selected documents from session state
        selected_docs = st.session_state.get('selected_documents', [])
        
        # First try to find relevant document chunks
        if selected_docs:
            # Search only in selected documents
            doc_paths = [os.path.join("uploaded_docs", doc) for doc in selected_docs]
            matches = search_index(query, specific_docs=doc_paths)
            doc_msg = f"Searched within {len(selected_docs)} selected documents"
        else:
            # Search all documents
            matches = search_index(query)
            doc_msg = "Searched all available documents"
        
        if matches and len(matches) > 0:
            # If we have relevant document matches, use them as context
            context = "\n\n".join([f"Document content: {match}" for match in matches])
            
            prompt = f"""
            Context information from company documents:
            {context}
            
            User question: {query}
            
            Based only on the context information provided, answer the user's question.
            If the answer cannot be directly found in the context, state that clearly.
            Begin your response with: "{doc_msg}"
            """
            
            return query_model(prompt, model_choice, api_key)
        else:
            # If no document matches, try FAQ
            faq_path = "faq.json"
            
            if os.path.exists(faq_path):
                with open(faq_path, "r") as f:
                    faq = json.load(f)
                
                # Look for matching FAQ questions
                for q, a in faq.items():
                    if q.lower() in query.lower() or query.lower() in q.lower():
                        return f"From FAQ:\n{a}"
            
            # If no FAQ matches either, let the AI try to answer generally
            prompt = f"""
            User question: {query}
            
            The user is asking about company information, but I couldn't find specific 
            documents or FAQ entries related to this question. 
            {doc_msg}, but no relevant information was found.
            
            Please provide a general response stating that you don't have specific 
            information on this topic and suggest what the user might do next.
            Begin your response with: "{doc_msg}, but no relevant information was found."
            """
            
            return query_model(prompt, model_choice, api_key)
    
    except Exception as e:
        return f"Sorry, I encountered an error while processing your request: {str(e)}"
