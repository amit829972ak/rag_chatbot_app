import streamlit as st
import hashlib

ADMIN_USER = "admin"
ADMIN_PASS = "admin123"

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def check_login(username, password):
    return username == ADMIN_USER and hash_password(password) == hash_password(ADMIN_PASS)

def login_form():
    with st.sidebar.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")
        if submitted:
            if check_login(username, password):
                st.session_state['authenticated'] = True
                st.success("Login successful")
            else:
                st.error("Invalid credentials")
