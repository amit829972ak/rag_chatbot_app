import streamlit as st
import hashlib
import os
import json
from datetime import datetime, timedelta

# File to store admin credentials
CREDENTIALS_FILE = "admin_credentials.json"

def initialize_credentials():
    """
    Initialize default admin credentials if credentials file doesn't exist.
    """
    if not os.path.exists(CREDENTIALS_FILE):
        # Default admin credentials
        default_password = "admin123"  # This is just a default, should be changed after first login
        hashed_password = hashlib.sha256(default_password.encode()).hexdigest()
        
        credentials = {
            "admin": {
                "password": hashed_password,
                "created_at": datetime.now().isoformat()
            }
        }
        
        with open(CREDENTIALS_FILE, "w") as f:
            json.dump(credentials, f, indent=4)

def verify_credentials(username, password):
    """
    Verify admin credentials.
    
    Args:
        username: Username to verify
        password: Password to verify
        
    Returns:
        bool: True if credentials are valid, False otherwise
    """
    # Initialize credentials if not already done
    if not os.path.exists(CREDENTIALS_FILE):
        initialize_credentials()
    
    try:
        # Read credentials from file
        with open(CREDENTIALS_FILE, "r") as f:
            credentials = json.load(f)
        
        # Check if username exists
        if username not in credentials:
            return False
        
        # Hash the provided password
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        
        # Compare with stored password
        return hashed_password == credentials[username]["password"]
    except (FileNotFoundError, json.JSONDecodeError, KeyError) as e:
        st.error(f"Error reading credentials: {e}")
        return False

def change_password(username, new_password):
    """
    Change admin password.
    
    Args:
        username: Username to change password for
        new_password: New password to set
        
    Returns:
        bool: True if password was changed successfully, False otherwise
    """
    # Initialize credentials if not already done
    if not os.path.exists(CREDENTIALS_FILE):
        initialize_credentials()
    
    try:
        # Read credentials from file
        with open(CREDENTIALS_FILE, "r") as f:
            credentials = json.load(f)
        
        # Check if username exists
        if username not in credentials:
            return False
        
        # Hash the new password
        hashed_password = hashlib.sha256(new_password.encode()).hexdigest()
        
        # Update the password
        credentials[username]["password"] = hashed_password
        credentials[username]["updated_at"] = datetime.now().isoformat()
        
        # Write credentials back to file
        with open(CREDENTIALS_FILE, "w") as f:
            json.dump(credentials, f, indent=4)
        
        return True
    except (FileNotFoundError, json.JSONDecodeError, KeyError) as e:
        st.error(f"Error changing password: {e}")
        return False

def login_form():
    """
    Display login form in Streamlit sidebar.
    
    Updates session state 'authenticated' to True if login is successful.
    """
    # Initialize credentials if not already done
    if not os.path.exists(CREDENTIALS_FILE):
        initialize_credentials()
    
    st.sidebar.subheader("Admin Login")
    
    # Login form
    username = st.sidebar.text_input("Username", value="admin")
    password = st.sidebar.text_input("Password", type="password")
    
    # Login button
    if st.sidebar.button("Login"):
        if verify_credentials(username, password):
            st.session_state['authenticated'] = True
            st.session_state['username'] = username  # Store username in session
            st.sidebar.success("Login successful!")
            st.rerun()  # Refresh the app to show authenticated state
        else:
            st.sidebar.error("Invalid username or password")

def change_password_form():
    """
    Display change password form in Streamlit sidebar.
    Uses username from session state.
    """
    if 'username' not in st.session_state:
        st.sidebar.error("Please login first")
        return
    
    username = st.session_state['username']
    
    st.sidebar.subheader("Change Password")
    
    # Change password form with unique keys
    current_password = st.sidebar.text_input("Current Password", type="password", key="current_pass")
    new_password = st.sidebar.text_input("New Password", type="password", key="new_pass")
    confirm_password = st.sidebar.text_input("Confirm New Password", type="password", key="confirm_pass")
    
    # Change password button
    if st.sidebar.button("Change Password", key="change_pass_btn"):
        # Verify current password first
        if not verify_credentials(username, current_password):
            st.sidebar.error("Current password is incorrect")
        elif new_password != confirm_password:
            st.sidebar.error("New passwords do not match")
        elif len(new_password) < 6:
            st.sidebar.error("Password must be at least 6 characters")
        elif new_password == current_password:
            st.sidebar.error("New password must be different from current password")
        else:
            if change_password(username, new_password):
                st.sidebar.success("Password changed successfully!")
                # Clear the form by rerunning
                st.rerun()
            else:
                st.sidebar.error("Failed to change password")

def logout():
    """
    Logout function to clear session state.
    """
    if st.sidebar.button("Logout"):
        st.session_state['authenticated'] = False
        if 'username' in st.session_state:
            del st.session_state['username']
        st.rerun()

# Main authentication handler
def handle_authentication():
    """
    Main function to handle authentication flow.
    Returns True if user is authenticated, False otherwise.
    """
    # Initialize session state
    if 'authenticated' not in st.session_state:
        st.session_state['authenticated'] = False
    
    # If not authenticated, show login form
    if not st.session_state['authenticated']:
        login_form()
        return False
    else:
        # If authenticated, show user info and options
        st.sidebar.success(f"Logged in as: {st.session_state.get('username', 'admin')}")
        
        # Show change password and logout options
        change_password_form()
        logout()
        
        return True

# Example usage in main app
def main():
    st.title("Admin Dashboard")
    
    # Handle authentication
    if not handle_authentication():
        st.info("Please login to access the admin dashboard.")
        return
    
    # Main app content (only shown if authenticated)
    st.write("Welcome to the admin dashboard!")
    st.write("You are successfully authenticated.")

if __name__ == "__main__":
    main()
