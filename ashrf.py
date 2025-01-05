import streamlit as st
import pandas as pd
from datetime import datetime
import json
import os

# File for saving persistent data
DATA_FILE = "machine_data.json"

# Initial machine data
default_data = {
    "machines": [
        {"No.": 1, "Terminal": "MOJ001", "Location": "Heliopolis", "First Operation": "2021-09-26", "Total Transactions": 0, "Last CIT": "19 Sep 2024", "No. Tickets": 109},
        {"No.": 2, "Terminal": "MOJ002", "Location": "South Cairo", "First Operation": "2021-05-05", "Total Transactions": 1634, "Last CIT": "23 Jul 2024", "No. Tickets": 66},
        {"No.": 3, "Terminal": "MOJ003", "Location": "North Cairo", "First Operation": "2021-05-20", "Total Transactions": 8876, "Last CIT": "19 Aug 2024", "No. Tickets": 43},
        {"No.": 4, "Terminal": "MOJ004", "Location": "East Alex", "First Operation": "2021-06-26", "Total Transactions": 0, "Last CIT": "16 Sep 2024", "No. Tickets": 91},
        {"No.": 5, "Terminal": "MOJ005", "Location": "West Alex", "First Operation": "2021-06-21", "Total Transactions": 244, "Last CIT": "10 Feb 2024", "No. Tickets": 44},
    ],
    "down_machines": ["MOJ003", "MOJ004", "MOJ005"],
    "comments": {},
}

# Load data from JSON file or initialize with defaults
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    else:
        return default_data

# Save data to JSON file
def save_data(data):
    with open(DATA_FILE, "w") as file:
        json.dump(data, file)

# Load data into session state
if "data" not in st.session_state:
    st.session_state.data = load_data()

machine_data = pd.DataFrame(st.session_state.data["machines"])
down_machines = set(st.session_state.data["down_machines"])
comments = st.session_state.data["comments"]

# Initialize session state for login
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "page" not in st.session_state:
    st.session_state.page = "login"
if "selected_machine" not in st.session_state:
    st.session_state.selected_machine = None

# Login Page
if st.session_state.page == "login":
    st.title("🔒 Login")
    st.markdown("""
        <style>
        .login-container {
            max-width: 400px;
            margin: auto;
            padding: 20px;
            border: 1px solid #ccc;
            border-radius: 10px;
            background-color: #f9f9f9;
            box-shadow: 2px 2px 8px rgba(0, 0, 0, 0.1);
        }
        .login-button {
            background-color: #4CAF50;
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }
        .login-button:hover {
            background-color: #45a049;
        }
        </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="login-container">', unsafe_allow_html=True)
    username = st.text_input("Username", placeholder="Enter your username")
    password = st.text_input("Password", type="password", placeholder="Enter your password")
    if st.button("Login", key="login_button", help="Click to login"):
        if username == "admin" and password == "123":
            st.success("Login successful!")
            st.session_state.logged_in = True
            st.session_state.page = "dashboard"
        else:
            st.error("Invalid username or password")
    st.markdown('</div>', unsafe_allow_html=True)

# Dashboard Page
if st.session_state.logged_in and st.session_state.page == "dashboard":
    st.title("📊 Machines Dashboard")

    # Summary Section
    st.subheader("Overview")
    col1, col2, col3 = st.columns(3)
    total_machines = len(machine_data)
    down_count = len(down_machines)
    up_count = total_machines - down_count
    col1.metric("Total Machines", total_machines)
    col2.metric("Up Machines", up_count)
    col3.metric("Down Machines", down_count)

    # Search Bar
    st.subheader("Search Machines")
    search_query = st.text_input("Search by Location or Terminal:")
    if search_query:
        filtered_data = machine_data[
            machine_data["Location"].str.contains(search_query, case=False, na=False)
            | machine_data["Terminal"].str.contains(search_query, case=False, na=False)
        ]
    else:
        filtered_data = machine_data

    # Machines Grid
    st.subheader("Machine List")
    cols = st.columns(2)
    for index, row in filtered_data.iterrows():
        col = cols[index % 2]
        status_color = "green" if row["Terminal"] not in down_machines else "red"
        comment_count = len(comments.get(row["Terminal"], []))
        with col:
            st.markdown(
                f"""
                <div style="border: 1px solid #ccc; padding: 10px; border-radius: 10px; background-color: #f9f9f9;">
                    <strong>{row['Location']}</strong><br>
                    Terminal: {row['Terminal']}<br>
                    Status: <span style="color:{status_color}; font-weight:bold;">{"Up" if row["Terminal"] not in down_machines else "Down"}</span><br>
                    Comments: {comment_count}<br>
                </div>
                """,
                unsafe_allow_html=True,
            )
            if st.button(f"View Details", key=row["Terminal"]):
                st.session_state.page = "details"
                st.session_state.selected_machine = row["Terminal"]

# Details Page
if st.session_state.logged_in and st.session_state.page == "details":
    selected_machine = st.session_state.selected_machine
    machine = machine_data[machine_data["Terminal"] == selected_machine].iloc[0]

    st.title(f"Details for {selected_machine}")

    # Machine Details
    st.subheader("Machine Information")
    for key, value in machine.items():
        st.write(f"**{key}:** {value}")

    # Change Status
    st.subheader("Update Status")
    current_status = "Down" if selected_machine in down_machines else "Up"
    new_status = st.radio("Change Status", ["Up", "Down"], index=0 if current_status == "Up" else 1)
    if st.button("Update Status"):
        if new_status == "Down":
            down_machines.add(selected_machine)
        else:
            down_machines.discard(selected_machine)
        st.session_state.data["down_machines"] = list(down_machines)
        save_data(st.session_state.data)
        st.success("Status updated successfully!")

    # Comments Section
    st.subheader("Comments")
    new_comment = st.text_area("Add Comment")
    if st.button("Submit Comment"):
        if selected_machine not in comments:
            comments[selected_machine] = []
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        comments[selected_machine].append(f"{timestamp}: {new_comment}")
        st.session_state.data["comments"] = comments
        save_data(st.session_state.data)
        st.success("Comment added successfully!")

    # Display Comments
    st.write("### Existing Comments:")
    for comment in comments.get(selected_machine, []):
        st.write(f"- {comment}")

    # Back Button
    if st.button("Back to Dashboard"):
        st.session_state.page = "dashboard"
