import streamlit as st
import pandas as pd
import os
import random

# Dummy user database
UAE_USERS = {
    "admin": {"password": "123", "role": "admin", "country": "both"},
    "murhaf": {"password": "123", "role": "user", "country": "UAE"},
    "khuram": {"password": "123", "role": "user", "country": "UAE"}
}

# Generate random 4-digit passwords for Egypt users
EGYPT_USERS = {
    "a.said": {"password": "123", "role": "user", "country": "Egypt"},
    "m.tarras": {"password": str(random.randint(1000, 9999)), "role": "user", "country": "Egypt"},
    "ashraf": {"password": str(random.randint(1000, 9999)), "role": "user", "country": "Egypt"},
    "islam": {"password": str(random.randint(1000, 9999)), "role": "user", "country": "Egypt"},
    "youssef": {"password": str(random.randint(1000, 9999)), "role": "user", "country": "Egypt"},
    "khaled": {"password": str(random.randint(1000, 9999)), "role": "user", "country": "Egypt"}
}

# Merge both user groups
USERS = {**UAE_USERS, **EGYPT_USERS}

TASK_FILE = "tasks.csv"  # File to store tasks

# Function to load tasks from CSV file
def load_tasks():
    if os.path.exists(TASK_FILE):
        df = pd.read_csv(TASK_FILE)
        if "Country" not in df.columns:
            df["Country"] = "UAE"  # Default to UAE if country is missing
        return df.to_dict(orient="records")
    return []

# Function to save tasks to CSV file
def save_tasks():
    if len(st.session_state.tasks) > 0:
        df = pd.DataFrame(st.session_state.tasks)
        df.to_csv(TASK_FILE, index=False)

# Initialize session state variables
if "tasks" not in st.session_state:
    st.session_state.tasks = load_tasks()

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.user = None
    st.session_state.role = None
    st.session_state.country = None

# Authentication function
def authenticate(username, password, country):
    if username in USERS and USERS[username]['password'] == password:
        if USERS[username]['country'] == country or USERS[username]['country'] == "both":
            st.session_state.user = username
            st.session_state.role = USERS[username]['role']
            st.session_state.country = USERS[username]['country']
            st.session_state.authenticated = True
            return True
    return False

# Logout function
def logout():
    st.session_state.authenticated = False
    st.session_state.user = None
    st.session_state.role = None
    st.session_state.country = None
    st.rerun()

# Delete Task Function (Only Admins can delete any task, Users can delete their own)
def delete_task(task_index):
    if st.session_state.role == "admin" or st.session_state.tasks[task_index]["User"] == st.session_state.user:
        del st.session_state.tasks[task_index]
        save_tasks()
        st.success("Task deleted successfully!")
        st.rerun()
    else:
        st.error("You don't have permission to delete this task.")

# Login Page with Country Selection
def login_page():
    st.title("🌍 Field Support Tracker")

    country = st.radio("Select your country:", ["UAE", "Egypt"], horizontal=True)
    
    username = st.text_input("👤 Username")
    password = st.text_input("🔑 Password", type="password")

    if st.button("Login", use_container_width=True):
        if authenticate(username, password, country):
            st.success(f"✅ Welcome, {username}!")
            st.rerun()
        else:
            st.error("❌ Invalid credentials or country mismatch.")

# Dashboard Page
def dashboard_page():
    st.title(f"📋 Dashboard - Welcome {st.session_state.user}")

    if st.session_state.role == "admin":
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

        # Extra Fields for Egypt Users
        moj_number = None
        uploaded_file = None
        if st.session_state.country == "Egypt":
            moj_number = st.text_input("🆔 MOJ Number (Mandatory for Egypt)")
            uploaded_file = st.file_uploader("📸 Upload Supporting Document")

        submit_button = st.form_submit_button("✅ Add Task")

        if submit_button:
            new_task = {
                "User": st.session_state.user,
                "Location": location,
                "Start Time": start_time.strftime("%Y-%m-%d"),
                "End Time": end_time.strftime("%Y-%m-%d"),
                "Description": description,
                "Status": status,
                "Comments": comments,
                "Country": st.session_state.country
            }

            # Only add MOJ and Image if Egypt user
            if st.session_state.country == "Egypt":
                if moj_number:
                    new_task["MOJ Number"] = moj_number
                if uploaded_file:
                    new_task["Document"] = uploaded_file.name  # Save file name

            st.session_state.tasks.append(new_task)
            save_tasks()
            st.success("Task added successfully!")
            st.rerun()

    # Load tasks into DataFrame
    if len(st.session_state.tasks) > 0:
        df_tasks = pd.DataFrame(st.session_state.tasks)

        # Ensure "Country" column exists before filtering
        if "Country" not in df_tasks.columns:
            df_tasks["Country"] = "UAE"  # Default all tasks to UAE if missing

        # Country-based filtering
        if st.session_state.role != "admin":
            df_tasks = df_tasks[df_tasks["Country"] == st.session_state.country]

        if "User" in df_tasks.columns:
            if selected_user != "All Users":
                df_tasks = df_tasks[df_tasks["User"] == selected_user]
        
        st.subheader("📌 Task List")

        for i, task in enumerate(df_tasks.to_dict(orient="records")):
            with st.expander(f"📌 Task {i+1}: {task['Description']} - {task['Status']}"):
                st.write(f"📍 **Location:** {task['Location']}")
                st.write(f"🕒 **Start Time:** {task['Start Time']}")
                st.write(f"⏳ **End Time:** {task['End Time']}")
                st.write(f"📝 **Description:** {task['Description']}")
                st.write(f"📌 **Status:** {task['Status']}")
                st.write(f"💬 **Comments:** {task['Comments']}")
                if "MOJ Number" in task:
                    st.write(f"🆔 **MOJ Number:** {task['MOJ Number']}")
                if "Document" in task:
                    st.write(f"📸 **Uploaded Document:** {task['Document']}")

                if st.session_state.role == "admin" or task["User"] == st.session_state.user:
                    if st.button(f"🗑️ Delete Task {i+1}", key=f"delete_{i}", use_container_width=True):
                        delete_task(i)

    else:
        st.warning("⚠️ No tasks available.")

    if st.button("🚪 Logout", use_container_width=True):
        logout()

# App Execution
if not st.session_state.authenticated:
    login_page()
else:
    dashboard_page()
