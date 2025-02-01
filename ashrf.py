import streamlit as st
import pandas as pd
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Gmail SMTP Configuration
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_SENDER = "ahmed.lgohary.am@gmail.com"
EMAIL_PASSWORD = "neyy gjxa cutv dswq"

# UAE User Database with Emails
UAE_USERS = {
    "admin": {"password": "123", "role": "admin", "country": "both", "email": "admin@example.com", "contact": "000-000-0000"},
    "murhaf": {"password": "123", "role": "user", "country": "UAE", "email": "murhaf@example.com", "contact": "111-111-1111"},
    "khuram": {"password": "123", "role": "user", "country": "UAE", "email": "khuram@example.com", "contact": "222-222-2222"}
}

# Updated Egypt User Database
EGYPT_USERS = {
    "mohamed_abdulghaffar": {"password": "123", "role": "user", "country": "Egypt", "email": "mohamedhashish660@gmail.com", "contact": "0100 2905148"},
    "youssef_taha": {"password": "123", "role": "user", "country": "Egypt", "email": "Youseftaha625@yahoo.com", "contact": "+20 106 0615876"},
    "ahmed_fawky": {"password": "123", "role": "user", "country": "Egypt", "email": "ahmadfawky@gmail.com", "contact": "0102 3128386"},
    "ahmed_said": {"password": "123", "role": "user", "country": "Egypt", "email": "ahmadsaid.eg40@gmail.com", "contact": "+20 111 7747737"},
    "moustafa_mamdouh": {"password": "123", "role": "user", "country": "Egypt", "email": "moustafa.mamdoh96@gmail.com", "contact": "0100 4471647"},
    "mohamed_ramadan": {"password": "123", "role": "user", "country": "Egypt", "email": "mohamedramadan1892@gmail.com", "contact": "0100 9837248"},
    "islam_sobhi": {"password": "123", "role": "user", "country": "Egypt", "email": "islamsobhy582@gmail.com", "contact": "+20 101 7790515"},
    "mohamed_korany": {"password": "123", "role": "user", "country": "Egypt", "email": "mokorany046@gmail.com", "contact": "0112 4705453"},
    "hossam_mostafa": {"password": "123", "role": "user", "country": "Egypt", "email": "hossammostafa066@gmail.com", "contact": "+20 106 6114964"},
    "amr_mahmoud": {"password": "123", "role": "user", "country": "Egypt", "email": "amr-mahmoud-87@hotmail.com", "contact": "0100 1027909"}
}

# Merge UAE & Egypt Users
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
            st.session_state.email = USERS[username]['email']
            st.session_state.contact = USERS[username]['contact']
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
    📝 Description: {task.get('Description', 'N/A')}
    📌 Status: {task.get('Status', 'N/A')}
    💬 Comments: {task.get('Comments', 'N/A')}
    🌍 Country: {task.get('Country', 'N/A')}
    📞 Contact Number: {USERS[task.get('Assigned To', '')]['contact']}
    """
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

# Dashboard Page
def dashboard_page():
    st.title(f"📋 Dashboard - Welcome {st.session_state.user}")

    st.subheader("👤 Your Info")
    st.write(f"📧 **Email:** {st.session_state.email}")
    st.write(f"📞 **Contact:** {st.session_state.contact}")

    st.subheader("➕ Add Task")
    with st.form("task_form"):
        if st.session_state.role == "admin":
            assigned_to = st.selectbox("👥 Assign Task To", list(USERS.keys()))
        else:
            assigned_to = st.session_state.user

        location = st.text_input("📍 Location")
        start_time = st.date_input("🕒 Start Date")
        end_time = st.date_input("⏳ End Date")
        description = st.text_area("📝 Description")
        status = st.selectbox("📌 Status", ["Pending", "In Progress", "Completed"])
        comments = st.text_area("💬 Comments")

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

            st.session_state.tasks.append(new_task)
            save_tasks()
            st.success(f"✅ Task assigned to {assigned_to}!")
            send_email_notification(new_task, USERS[assigned_to]["email"])
            st.rerun()

    st.subheader("📌 Task List")
    if len(st.session_state.tasks) > 0:
        df_tasks = pd.DataFrame(st.session_state.tasks)
        if st.session_state.role != "admin":
            df_tasks = df_tasks[df_tasks.get("Assigned To", "") == st.session_state.user]

        st.dataframe(df_tasks)
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
