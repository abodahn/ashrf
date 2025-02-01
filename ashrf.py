import streamlit as st
import pandas as pd
import os
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Gmail SMTP Configuration
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_SENDER = "ahmed.lgohary.am@gmail.com"
EMAIL_PASSWORD = "neyy gjxa cutv dswq"

# User Database with Emails
UAE_USERS = {
    "admin": {"password": "123", "role": "admin", "country": "both", "email": "admin@example.com"},
    "murhaf": {"password": "123", "role": "user", "country": "UAE", "email": "murhaf@example.com"},
    "khuram": {"password": "123", "role": "user", "country": "UAE", "email": "khuram@example.com"}
}

EGYPT_USERS = {
    "a.said": {"password": str(random.randint(1000, 9999)), "role": "user", "country": "Egypt", "email": "asaid@example.com"},
    "m.tarras": {"password": str(random.randint(1000, 9999)), "role": "user", "country": "Egypt", "email": "mtarras@example.com"},
    "ashraf": {"password": str(random.randint(1000, 9999)), "role": "user", "country": "Egypt", "email": "ashraf@example.com"},
    "islam": {"password": str(random.randint(1000, 9999)), "role": "user", "country": "Egypt", "email": "islam@example.com"},
    "youssef": {"password": str(random.randint(1000, 9999)), "role": "user", "country": "Egypt", "email": "youssef@example.com"},
    "khaled": {"password": str(random.randint(1000, 9999)), "role": "user", "country": "Egypt", "email": "khaled@example.com"}
}

# Merge UAE & Egypt users
USERS = {**UAE_USERS, **EGYPT_USERS}

# Load Tasks from CSV
TASK_FILE = "tasks.csv"
def load_tasks():
    if os.path.exists(TASK_FILE):
        return pd.read_csv(TASK_FILE).to_dict(orient="records")
    return []

# Save Tasks to CSV
def save_tasks():
    if len(st.session_state.tasks) > 0:
        df = pd.DataFrame(st.session_state.tasks)
        df.to_csv(TASK_FILE, index=False)

# Initialize Session State
if "tasks" not in st.session_state:
    st.session_state.tasks = load_tasks()
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.user = None
    st.session_state.role = None
    st.session_state.country = None

# Authentication Function
def authenticate(username, password, country):
    if username in USERS and USERS[username]['password'] == password:
        if USERS[username]['country'] == country or USERS[username]['country'] == "both":
            st.session_state.user = username
            st.session_state.role = USERS[username]['role']
            st.session_state.country = USERS[username]['country']
            st.session_state.authenticated = True
            return True
    return False

# Logout Function
def logout():
    st.session_state.authenticated = False
    st.session_state.user = None
    st.session_state.role = None
    st.session_state.country = None
    st.rerun()

# Send Email Notification
def send_email_notification(task, user_email):
    subject = f"New Task Assigned to {task['User']}"
    message = f"""
    Hello {task['User']},

    A new task has been assigned to you:

    📍 Location: {task['Location']}
    🕒 Start Time: {task['Start Time']}
    ⏳ End Time: {task['End Time']}
    📝 Description: {task['Description']}
    📌 Status: {task['Status']}
    💬 Comments: {task['Comments']}
    🌍 Country: {task['Country']}
    """
    if "MOJ Number" in task:
        message += f"🆔 MOJ Number: {task['MOJ Number']}\n"

    msg = MIMEMultipart()
    msg["From"] = EMAIL_SENDER
    msg["To"] = user_email
    msg["Subject"] = subject
    msg.attach(MIMEText(message, "plain"))

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_SENDER, user_email, msg.as_string())
        server.quit()
        st.success(f"📧 Email sent successfully to {user_email}!")
    except Exception as e:
        st.error(f"❌ Failed to send email: {e}")

# Delete Task Function
def delete_task(index):
    if st.session_state.role == "admin" or st.session_state.tasks[index]["User"] == st.session_state.user:
        del st.session_state.tasks[index]
        save_tasks()
        st.success("🗑️ Task deleted successfully!")
        st.rerun()
    else:
        st.error("❌ You don't have permission to delete this task.")

# Dashboard Page
def dashboard_page():
    st.title(f"📋 Dashboard - Welcome {st.session_state.user}")

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
            if st.session_state.country == "Egypt":
                new_task["MOJ Number"] = moj_number
                new_task["Document"] = uploaded_file.name if uploaded_file else "No File"

            st.session_state.tasks.append(new_task)
            save_tasks()
            send_email_notification(new_task, USERS[st.session_state.user]["email"])
            st.success("Task added successfully!")
            st.rerun()

    # Display Task List
    st.subheader("📌 Task List")
    if len(st.session_state.tasks) > 0:
        df_tasks = pd.DataFrame(st.session_state.tasks)

        # Filter tasks by country unless admin
        if st.session_state.role != "admin":
            df_tasks = df_tasks[df_tasks["Country"] == st.session_state.country]

        for index, task in enumerate(df_tasks.to_dict(orient="records")):
            with st.expander(f"📍 {task['Location']} - {task['Description']}"):
                st.write(f"🕒 **Start Time:** {task['Start Time']}")
                st.write(f"⏳ **End Time:** {task['End Time']}")
                st.write(f"📌 **Status:** {task['Status']}")
                st.write(f"💬 **Comments:** {task['Comments']}")
                if "MOJ Number" in task:
                    st.write(f"🆔 **MOJ Number:** {task['MOJ Number']}")
                if "Document" in task:
                    st.write(f"📸 **Document:** {task['Document']}")

                # Delete Button (Admins or Task Owner)
                if st.session_state.role == "admin" or task["User"] == st.session_state.user:
                    if st.button(f"🗑️ Delete Task", key=f"delete_{index}"):
                        delete_task(index)
    else:
        st.warning("⚠️ No tasks available.")

    if st.button("🚪 Logout", use_container_width=True):
        logout()

# Login Page
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

# Run Streamlit App
if not st.session_state.authenticated:
    login_page()
else:
    dashboard_page()
