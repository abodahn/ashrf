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
    ],
    "down_machines": ["MOJ003", "MOJ004", "MOJ005"],
    "comments": {}
}

# User credentials
credentials = {
    "admin": "123",
    "ashraf": "1234",
    "ahmed": "123456"
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

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = None

if not st.session_state.logged_in:
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username in credentials and credentials[username] == password:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success(f"Welcome, {username}!")
        else:
            st.error("Invalid username or password.")
else:
    machine_data = pd.DataFrame(st.session_state.data["machines"])
    down_machines = set(st.session_state.data["down_machines"])
    comments = st.session_state.data["comments"]

    # Initialize session state for navigation
    if "page" not in st.session_state:
        st.session_state.page = "dashboard"
    if "selected_machine" not in st.session_state:
        st.session_state.selected_machine = None

    # Sidebar Reset Button
    if st.sidebar.button("Reset Data"):
        save_data(default_data)
        st.session_state.data = default_data
        st.success("Data has been reset!")

    # Dashboard Page
    if st.session_state.page == "dashboard":
        st.title("📊 Machines Dashboard")

        # Summary Section
        st.subheader("Overview")
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Machines", len(machine_data))
        col2.metric("Up Machines", len(machine_data) - len(down_machines))
        col3.metric("Down Machines", len(down_machines))

        # Search Bar
        search_query = st.text_input("Search by Location or Terminal")
        filtered_data = machine_data[
            machine_data["Location"].str.contains(search_query, case=False, na=False)
            | machine_data["Terminal"].str.contains(search_query, case=False, na=False)
        ] if search_query else machine_data

        # Machines Grid
        st.subheader("Machine List")
        cols = st.columns(2)  # Two columns for displaying cards
        for index, row in filtered_data.iterrows():
            col = cols[index % 2]
            status_color = "green" if row["Terminal"] not in down_machines else "red"
            with col:
                st.markdown(
                    f"""
                    <div style="border: 1px solid #ddd; padding: 10px; margin: 5px; border-radius: 10px; background-color: #f9f9f9;">
                        <strong>{row['Location']}</strong><br>
                        Terminal: {row['Terminal']}<br>
                        Status: <span style="color:{status_color}; font-weight:bold;">{"Up" if row["Terminal"] not in down_machines else "Down"}</span><br>
                        Total Transactions: {row['Total Transactions']}<br>
                        Last CIT: {row['Last CIT']}<br>
                        Tickets: {row['No. Tickets']}
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                if st.button(f"View Details: {row['Terminal']}", key=f"view_{row['Terminal']}"):
                    st.session_state.selected_machine = row["Terminal"]
                    st.session_state.page = "details"

    # Details Page
    if st.session_state.page == "details":
        selected_terminal = st.session_state.selected_machine
        machine = machine_data[machine_data["Terminal"] == selected_terminal].iloc[0]

        st.title(f"Details for {selected_terminal}")

        # Machine Details
        st.subheader("Machine Information")
        for key, value in machine.items():
            st.write(f"**{key}:** {value}")

        # Update Machine Status
        st.subheader("Update Machine Status")
        current_status = "Down" if selected_terminal in down_machines else "Up"
        new_status = st.radio("Change Status", ["Up", "Down"], index=0 if current_status == "Up" else 1)
        if st.button("Update Status"):
            if new_status == "Down":
                down_machines.add(selected_terminal)
            else:
                down_machines.discard(selected_terminal)
            st.session_state.data["down_machines"] = list(down_machines)
            save_data(st.session_state.data)
            st.success("Status updated successfully!")

        # Editable Fields
        st.subheader("Update Fields")
        new_tickets = st.number_input("Update No. Tickets", value=machine["No. Tickets"])
        new_transactions = st.number_input("Update Total Transactions", value=machine["Total Transactions"])
        new_cit = st.text_input("Update Last CIT", value=machine["Last CIT"])
        if st.button("Save Updates"):
            machine_data.loc[machine_data["Terminal"] == selected_terminal, "No. Tickets"] = new_tickets
            machine_data.loc[machine_data["Terminal"] == selected_terminal, "Total Transactions"] = new_transactions
            machine_data.loc[machine_data["Terminal"] == selected_terminal, "Last CIT"] = new_cit
            st.session_state.data["machines"] = machine_data.to_dict("records")
            save_data(st.session_state.data)
            st.success("Machine details updated successfully!")

        # Comments Section
        st.subheader("Comments")
        new_comment = st.text_area("Add a Comment")
        if st.button("Submit Comment"):
            if selected_terminal not in comments:
                comments[selected_terminal] = []
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            comments[selected_terminal].append(f"{timestamp} ({st.session_state.username}): {new_comment}")
            st.session_state.data["comments"] = comments
            save_data(st.session_state.data)
            st.success("Comment added successfully!")

        # Display Comments
        st.subheader("Existing Comments")
        for comment in comments.get(selected_terminal, []):
            st.write(f"- {comment}")

        # Back to Dashboard
        if st.button("Back to Dashboard"):
            st.session_state.page = "dashboard"
