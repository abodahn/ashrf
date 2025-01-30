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
EMAIL_SENDER = "ahmed.lgohary.am@gmail.com"  # ✅ Your Gmail Address
EMAIL_PASSWORD = "neyy gjxa cutv dswq"  # ✅ Your Google App Password

# ✅ User Database with Emails
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

# ✅ Function to send an email notification to the assigned user
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
        server.starttls()  # ✅ Enable TLS encryption
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_SENDER, user_email, msg.as_string())
        server.quit()
        st.success(f"📧 Email sent successfully to {user_email}!")
    except Exception as e:
        st.error(f"❌ Failed to send email to {user_email}: {e}")

# ✅ Function to simulate task creation (Modify this in your real app)
def add_task():
    task = {
        "User": "murhaf",  # Example user
        "Location": "Dubai",
        "Start Time": "2024-01-30",
        "End Time": "2024-02-01",
        "Description": "Fix network issue",
        "Status": "In Progress",
        "Comments": "Urgent",
        "Country": "UAE"
    }

    # ✅ Get the email of the assigned user
    user_email = USERS[task["User"]]["email"]

    # ✅ Send the email to the user
    send_email_notification(task, user_email)

# ✅ Streamlit Button to Test Email Notification for Users
st.title("📧 Test Email Notification")
if st.button("Send Test Email to User"):
    add_task()
