import streamlit as st
import pandas as pd

# Dummy user database
USERS = {
    "admin": {"password": "123", "role": "admin"},
    "murhaf": {"password": "123", "role": "user"},
    "khuram": {"password": "123", "role": "user"}
}

# Initialize task storage in session state
if "tasks" not in st.session_state:
    st.session_state.tasks = []

# Authentication function
def authenticate(username, password):
    if username in USERS and USERS[username]['password'] == password:
        st.session_state.user = username
        st.session_state.role = USERS[username]['role']
        st.session_state.authenticated = True
        return True
    return False

# Logout function
def logout():
    st.session_state.authenticated = False
    st.session_state.user = None
    st.session_state.role = None
    st.rerun()

# Login Page
def login_page():
    st.title("Field Support Tracker")
    
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        if authenticate(username, password):
            st.success(f"Welcome, {username}!")
            st.rerun()
        else:
            st.error("Invalid credentials. Try again.")

# Dashboard Page
def dashboard_page():
    st.title(f"Dashboard - Welcome {st.session_state.user}")

    if st.session_state.role == "admin":
        selected_user = st.selectbox("Filter by User", ["All Users"] + list(USERS.keys()))
    else:
        selected_user = st.session_state.user

    st.subheader("Add Task")
    with st.form("task_form"):
        location = st.text_input("Location")
        start_time = st.text_input("Start Time")
        end_time = st.text_input("End Time")
        description = st.text_input("Description")
        status = st.text_input("Status")
        comments = st.text_input("Comments")
        
        submit_button = st.form_submit_button("Add Task")

        if submit_button:
            new_task = {
                "User": st.session_state.user,  # Ensure "User" column exists
                "Location": location,
                "Start Time": start_time,
                "End Time": end_time,
                "Description": description,
                "Status": status,
                "Comments": comments
            }
            st.session_state.tasks.append(new_task)
            st.success("Task added successfully!")
            st.rerun()

    # Ensure there is at least one task before creating the DataFrame
    if len(st.session_state.tasks) > 0:
        df_tasks = pd.DataFrame(st.session_state.tasks)

        # Ensure "User" column exists before filtering
        if "User" in df_tasks.columns:
            if selected_user != "All Users":
                df_tasks = df_tasks[df_tasks["User"] == selected_user]
        
        st.subheader("Task List")
        st.dataframe(df_tasks)
    else:
        st.warning("No tasks available.")

    # Logout button
    if st.button("Logout"):
        logout()

# App Execution
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    login_page()
else:
    dashboard_page()
