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

# User Database with Emails and Contact Numbers
UAE_USERS = {
    "admin": {"password": "123", "role": "admin", "country": "both", "email": "admin@example.com", "contact": "0000"},
    "murhaf": {"password": "123", "role": "user", "country": "UAE", "email": "murhaf@example.com", "contact": "1111"},
    "khuram": {"password": "123", "role": "user", "country": "UAE", "email": "khuram@example.com", "contact": "2222"}
}

EGYPT_USERS = {
    "m.abdulghaffar": {"password": "123", "role": "user", "country": "Egypt", "email": "mohamedhashish660@gmail.com", "contact": "0100 2905148"},
    "y.taha": {"password": "123", "role": "user", "country": "Egypt", "email": "Youseftaha625@yahoo.com", "contact": "+20 106 0615876"},
    "a.fawky": {"password": "123", "role": "user", "country": "Egypt", "email": "ahmadfawky@gmail.com", "contact": "0102 3128386"},
    "a.said": {"password": "123", "role": "user", "country": "Egypt", "email": "ahmadsaid.eg40@gmail.com", "contact": "+20 111 7747737"},
    "m.mamdouh": {"password": "123", "role": "user", "country": "Egypt", "email": "moustafa.mamdoh96@gmail.com", "contact": "0100 4471647"},
    "m.ramadan": {"password": "123", "role": "user", "country": "Egypt", "email": "mohamedramadan1892@gmail.com", "contact": "0100 9837248"},
    "i.sobhi": {"password": "123", "role": "user", "country": "Egypt", "email": "islamsobhy582@gmail.com", "contact": "+20 101 7790515"},
    "m.korany": {"password": "123", "role": "user", "country": "Egypt", "email": "mokorany046@gmail.com", "contact": "0112 4705453"},
    "h.mostafa": {"password": "123", "role": "user", "country": "Egypt", "email": "hossammostafa066@gmail.com", "contact": "+20 106 6114964"},
    "a.mahmoud": {"password": "123", "role": "user", "country": "Egypt", "email": "amr-mahmoud-87@hotmail.com", "contact": "0100 1027909"}
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
    subject = f"New Task Assigned to {task.get('Assigned To', 'Unknown')}"
    message = f"""
    Hello {task.get('Assigned To', 'User')},

    A new task has been assigned to you:

    📍 Location: {task.get('Location', 'N/A')}
    🕒 Start Time: {task.get('Start Time', 'N/A')}
    ⏳ End Time: {task.get('End Time', 'N/A')}
    🗒️ Description: {task.get('Description', 'N/A')}
    📌 Status: {task.get('Status', 'N/A')}
    💬 Comments: {task.get('Comments', 'N/A')}
    🌍 Country: {task.get('Country', 'N/A')}
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
    del st.session_state.tasks[index]
    save_tasks()
    st.success("🗑️ Task deleted successfully!")
    st.rerun()

# Update Task Function
def update_task(index, status, note):
    st.session_state.tasks[index]["Status"] = status
    st.session_state.tasks[index]["Comments"] += f"\nNote: {note}"
    save_tasks()
    st.success("📊 Task updated successfully!")
    st.rerun()

# Dashboard Page
def dashboard_page():
    st.title(f"📋 Dashboard - Welcome {st.session_state.user}")

    st.subheader("➕ Add Task")
    with st.form("task_form"):
        assigned_to = st.selectbox("👥 Assign Task To", list(USERS.keys()))

        location = st.text_input("📍 Location")
        start_time = st.date_input("🕒 Start Date")
        end_time = st.date_input("⏳ End Date")
        description = st.text_area("🗒️ Description")
        status = st.selectbox("📌 Status", ["On hold", "In Progress", "Completed"])
        comments = st.text_area("💬 Comments")

        moj_number = None
        uploaded_file = None
        if USERS[assigned_to]["country"] == "Egypt":
            moj_number = st.text_input("🆔 MOJ Number (Mandatory for Egypt)")
            uploaded_file = st.file_uploader("📸 Upload Supporting Document")

        submit_button = st.form_submit_button("✅ Add Task")

        if submit_button:
            new_task = {
                "Assigned By": st.session_state.user,
                "Assigned To": assigned_to,
                "Location": location,
                "Start Time": start_time.strftime("%Y-%m-%d"),
                "End Time": end_time.strftime("%Y-%m-%d"),
                "Description": description,
                "Status": status,
                "Comments": comments,
                "Country": USERS[assigned_to]["country"]
            }
            if USERS[assigned_to]["country"] == "Egypt":
                new_task["MOJ Number"] = moj_number
                new_task["Document"] = uploaded_file.name if uploaded_file else "No File"

            st.session_state.tasks.append(new_task)
            save_tasks()
            st.success(f"✅ Task assigned to {assigned_to}!")
            st.rerun()

    st.subheader("📌 Task List")
    if len(st.session_state.tasks) > 0:
        df_tasks = pd.DataFrame(st.session_state.tasks)

        for index, task in enumerate(df_tasks.to_dict(orient="records")):
            assigned_to = task.get('Assigned To', 'Unknown')
            assigned_by = task.get('Assigned By', 'Unknown')
            location = task.get('Location', 'No Location')
            description = task.get('Description', 'No Description')

            with st.expander(f"📍 {location} - {description}"):
                st.write(f"👥 **Assigned To:** {assigned_to}")
                st.write(f"📞 **Contact Number:** {USERS.get(assigned_to, {}).get('contact', 'N/A')}")
                st.write(f"👤 **Assigned By:** {assigned_by}")
                st.write(f"🕒 **Start Time:** {task.get('Start Time', 'N/A')}")
                st.write(f"⏳ **End Time:** {task.get('End Time', 'N/A')}")
                st.write(f"📌 **Status:** {task.get('Status', 'N/A')}")
                st.write(f"💬 **Comments:** {task.get('Comments', 'N/A')}")

                if "MOJ Number" in task:
                    st.write(f"🆔 **MOJ Number:** {task['MOJ Number']}")
                if "Document" in task:
                    st.write(f"📸 **Document:** {task['Document']}")

                with st.form(f"update_form_{index}"):
                    new_status = st.selectbox("Update Status", ["On hold", "In Progress", "Completed"], index=["On hold", "In Progress", "Completed"].index(task.get('Status', 'On hold')))
                    note = st.text_area("Add Note")
                    update_button = st.form_submit_button("Update Task")
                    if update_button:
                        update_task(index, new_status, note)

                if st.button(f"📧 Send Email to {assigned_to}", key=f"email_{index}"):
                    send_email_notification(task, USERS.get(assigned_to, {}).get("email", ""))

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
