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
        {"No.": 6, "Terminal": "MOJ006", "Location": "North Damanhour", "First Operation": "2021-06-26", "Total Transactions": 6203, "Last CIT": "9 Sep 2024", "No. Tickets": 146},
        {"No.": 7, "Terminal": "MOJ007", "Location": "High Court", "First Operation": "2021-10-07", "Total Transactions": 964, "Last CIT": "27 May 2024", "No. Tickets": 26},
        {"No.": 8, "Terminal": "MOJ008", "Location": "South Giza", "First Operation": "2021-06-28", "Total Transactions": 2335, "Last CIT": "20 May 2024", "No. Tickets": 41},
        {"No.": 9, "Terminal": "MOJ009", "Location": "North Banha", "First Operation": "2021-07-14", "Total Transactions": 3520, "Last CIT": "11 Sep 2024", "No. Tickets": 72},
        {"No.": 10, "Terminal": "MOJ010", "Location": "South Banha", "First Operation": "2021-07-14", "Total Transactions": 2947, "Last CIT": "18 Jul 2024", "No. Tickets": 68},
        {"No.": 11, "Terminal": "MOJ011", "Location": "North Giza", "First Operation": "2021-05-07", "Total Transactions": 1255, "Last CIT": "31 Jan 2024", "No. Tickets": 41},
        {"No.": 12, "Terminal": "MOJ012", "Location": "Sharm El Sheikh", "First Operation": "2022-02-03", "Total Transactions": 554, "Last CIT": "7 Aug 2024", "No. Tickets": 16},
        {"No.": 13, "Terminal": "MOJ013", "Location": "City Stars", "First Operation": "2021-12-20", "Total Transactions": 45, "Last CIT": "3 Apr 2024", "No. Tickets": 14},
        {"No.": 14, "Terminal": "MOJ014", "Location": "Bank Misr Mohamed Farid", "First Operation": "2022-09-02", "Total Transactions": 46, "Last CIT": "28 Feb 2024", "No. Tickets": 5},
        {"No.": 15, "Terminal": "MOJ015", "Location": "Hurghada", "First Operation": "2022-02-13", "Total Transactions": 285, "Last CIT": "17 Jan 2024", "No. Tickets": 16},
        {"No.": 16, "Terminal": "MOJ016", "Location": "Luxor", "First Operation": "2022-02-14", "Total Transactions": 6, "Last CIT": "7 Jul 2024", "No. Tickets": 9},
        {"No.": 17, "Terminal": "MOJ017", "Location": "Sohag", "First Operation": "2022-02-15", "Total Transactions": 19181, "Last CIT": "28 Aug 2024", "No. Tickets": 154},
        {"No.": 18, "Terminal": "MOJ018", "Location": "Al Minya", "First Operation": "2022-02-17", "Total Transactions": 6375, "Last CIT": "29 Aug 2024", "No. Tickets": 145},
        {"No.": 19, "Terminal": "MOJ019", "Location": "Port Said", "First Operation": "2022-03-13", "Total Transactions": 1743, "Last CIT": "24 Mar 2024", "No. Tickets": 27},
        {"No.": 20, "Terminal": "MOJ020", "Location": "Ismaillia", "First Operation": "2022-03-14", "Total Transactions": 475, "Last CIT": "12 Aug 2024", "No. Tickets": 61},
        {"No.": 21, "Terminal": "MOJ021", "Location": "Suez", "First Operation": "2022-03-15", "Total Transactions": 1005, "Last CIT": "5 Feb 2024", "No. Tickets": 31},
        {"No.": 22, "Terminal": "MOJ022", "Location": "Fayoum", "First Operation": "2022-03-16", "Total Transactions": 1624, "Last CIT": "14 Aug 2024", "No. Tickets": 137},
        {"No.": 23, "Terminal": "MOJ023", "Location": "South Mansoura", "First Operation": "2022-03-17", "Total Transactions": 2273, "Last CIT": "21 Oct 2023", "No. Tickets": 11},
        {"No.": 24, "Terminal": "MOJ024", "Location": "North Zagazig", "First Operation": "2022-06-08", "Total Transactions": 1327, "Last CIT": "11 Nov 2023", "No. Tickets": 32},
        {"No.": 25, "Terminal": "MOJ025", "Location": "South Zagazig", "First Operation": "2022-07-08", "Total Transactions": 2135, "Last CIT": "29 May 2024", "No. Tickets": 89},
        {"No.": 26, "Terminal": "MOJ026", "Location": "Shebin El Koum", "First Operation": "2022-09-08", "Total Transactions": 1673, "Last CIT": "29 Sep 2024", "No. Tickets": 85},
        {"No.": 27, "Terminal": "MOJ027", "Location": "Marsa Matrouh", "First Operation": "2022-10-08", "Total Transactions": 2, "Last CIT": "6 Aug 2024", "No. Tickets": 7},
        {"No.": 28, "Terminal": "MOJ028", "Location": "North Mansoura", "First Operation": "2022-06-11", "Total Transactions": 75, "Last CIT": "28 Jan 2024", "No. Tickets": 11},
        {"No.": 29, "Terminal": "MOJ029", "Location": "New Cairo", "First Operation": "2023-12-08", "Total Transactions": 51, "Last CIT": "21 Jul 2024", "No. Tickets": 43},
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

# Reset Button
if st.sidebar.button("Reset Data"):
    save_data(default_data)
    st.session_state.data = default_data
    st.success("Data has been reset!")

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
    username = st.text_input("Username", placeholder="Enter your username")
    password = st.text_input("Password", type="password", placeholder="Enter your password")
    if st.button("Login"):
        if username == "admin" and password == "123":
            st.success("Login successful!")
            st.session_state.logged_in = True
            st.session_state.page = "dashboard"
        else:
            st.error("Invalid username or password")

# Dashboard Page
if st.session_state.logged_in and st.session_state.page == "dashboard":
    st.title("📊 Machines Dashboard")

    # Summary Section
    st.subheader("Overview")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Machines", len(machine_data))
    col2.metric("Up Machines", len(machine_data) - len(down_machines))
    col3.metric("Down Machines", len(down_machines))

    # Search Bar
    search_query = st.text_input("Search by Location or Terminal")
    if search_query:
        filtered_data = machine_data[
            machine_data["Location"].str.contains(search_query, case=False, na=False)
            | machine_data["Terminal"].str.contains(search_query, case=False, na=False)
        ]
    else:
        filtered_data = machine_data

    # Display Machines
    for _, row in filtered_data.iterrows():
        st.markdown(f"""
            - **{row['Location']}**: {row['Terminal']}
            - **Status**: {"Up" if row['Terminal'] not in down_machines else "Down"}
        """)

# Details Page
if st.session_state.logged_in and st.session_state.page == "details":
    st.write("Details page not implemented yet.")
