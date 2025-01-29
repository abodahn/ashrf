import streamlit as st
import pandas as pd
import os

# Dummy user database
USERS = {
    "Admin": {"password": "123", "role": "Admin"},
    "murhaf": {"password": "123", "role": "user"},
    "khuram": {"password": "123", "role": "user"}
}

TASK_FILE = "tasks.csv"  # File to store tasks

# Function to load tasks from CSV file
def load_tasks():
    if os.path.exists(TASK_FILE):
        return pd.read_csv(TASK_FILE).to_dict(orient="records")
    return []

# Function to save tasks to CSV file
def save_tasks():
    df = pd.DataFrame(st.session_state.tasks)
    df.to_csv(TASK_FILE, index=False)

# Initialize session state variables
if "tasks" not in st.session_state:
    st.session_state.tasks = load_tasks()  # Load existing tasks

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.user = None
    st.session_state.role = None

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

# Delete Task Function (Only Admins can delete any task, Users can delete their own)
def delete_task(task_index):
    if st.session_state.role == "Admin" or st.session_state.tasks[task_index]["User"] == st.session_state.user:
        del st.session_state.tasks[task_index]
        save_tasks()
        st.success("Task deleted successfully!")
        st.rerun()
    else:
        st.error("You don't have permission to delete this task.")

# Login Page
def login_page():
    st.title("🔐 Field Support Tracker")
    
    username = st.text_input("👤 Username")
    password = st.text_input("🔑 Password", type="password")
    
    if st.button("Login", use_container_width=True):
        if authenticate(username, password):
            st.success(f"✅ Welcome, {username}!")
            st.rerun()
        else:
            st.error("❌ Invalid credentials. Try again.")

# Dashboard Page
def dashboard_page():
    st.title(f"📋 Dashboard - Welcome {st.session_state.user}")

    if st.session_state.role == "Admin":
        selected_user = st.selectbox("👥 Filter by User", ["All Users"] + list(USERS.keys()))
    else:
        selected_user = st.session_state.user

    st.subheader("➕ Add Task")
    with st.form("task_form"):
        location = st.text_input("📍 Location")
        start_time = st.date_input("🕒 Start Date")
        end_time = st.date_input("⏳ End Date")
        description = st.text_area("📝 Description")
        status = st.selectbox("📌 Status", ["Pending", "In Progress", "Completed"])
        comments = st.text_area("💬 Comments")
        
        submit_button = st.form_submit_button("✅ Add Task")

        if submit_button:
            new_task = {
                "User": st.session_state.user,
                "Location": location,
                "Start Time": start_time.strftime("%Y-%m-%d"),
                "End Time": end_time.strftime("%Y-%m-%d"),
                "Description": description,
                "Status": status,
                "Comments": comments
            }
            st.session_state.tasks.append(new_task)
            save_tasks()
            st.success("Task added successfully!")
            st.rerun()

    # Load tasks into DataFrame
    if len(st.session_state.tasks) > 0:
        df_tasks = pd.DataFrame(st.session_state.tasks)

        if "User" in df_tasks.columns:
            if selected_user != "All Users":
                df_tasks = df_tasks[df_tasks["User"] == selected_user]
        
        st.subheader("📌 Task List")
        
        # Display Task Table with Delete Buttons
        for i, task in enumerate(df_tasks.to_dict(orient="records")):
            with st.expander(f"📌 Task {i+1}: {task['Description']} - {task['Status']}"):
                st.write(f"📍 **Location:** {task['Location']}")
                st.write(f"🕒 **Start Time:** {task['Start Time']}")
                st.write(f"⏳ **End Time:** {task['End Time']}")
                st.write(f"📝 **Description:** {task['Description']}")
                st.write(f"📌 **Status:** {task['Status']}")
                st.write(f"💬 **Comments:** {task['Comments']}")

                # Delete button (Only allow if Admin or the owner)
                if st.session_state.role == "Admin" or task["User"] == st.session_state.user:
                    if st.button(f"🗑️ Delete Task {i+1}", key=f"delete_{i}", use_container_width=True):
                        delete_task(i)

        # Status Pie Chart
        st.subheader("📊 Task Status Overview")
        status_counts = df_tasks["Status"].value_counts()
        st.bar_chart(status_counts)

    else:
        st.warning("⚠️ No tasks available.")

    # Logout button
    if st.button("🚪 Logout", use_container_width=True):
        logout()

# App Execution
if not st.session_state.authenticated:
    login_page()
else:
    dashboard_page()
