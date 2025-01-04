import streamlit as st
import pandas as pd

# Hardcoded credentials
MAIN_USERNAME = 'admin'
MAIN_PASSWORD = '1234'
UPDATE_PASSWORD = '12'

# Hardcoded data (replacing the Excel file)
data = [
    {"No.": 1, "Terminal": "MOJ001", "Location": "Heliopolis", "First Operation": "2021-09-26", "Total Transactions": 0, "Last CIT": "19 Sep 2024", "No. Tickets": 109},
    {"No.": 2, "Terminal": "MOJ002", "Location": "South Cairo", "First Operation": "2021-05-05", "Total Transactions": 1634, "Last CIT": "23 Jul 2024", "No. Tickets": 66},
    {"No.": 3, "Terminal": "MOJ003", "Location": "North Cairo", "First Operation": "2021-05-20", "Total Transactions": 8876, "Last CIT": "19 Aug 2024", "No. Tickets": 43},
    {"No.": 4, "Terminal": "MOJ004", "Location": "East Alex", "First Operation": "2021-06-26", "Total Transactions": 0, "Last CIT": "16 Sep 2024", "No. Tickets": 91},
    # Add all rows here based on your data
]

# Convert hardcoded data into a Pandas DataFrame
machine_data = pd.DataFrame(data)

# Machines with a "down" status
down_machines = {'MOJ015', 'MOJ018', 'MOJ021', 'MOJ023', 'MOJ024'}

# Dictionary to store comments for each machine
comments = {}

# Login Page
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.title("MOJ Project Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username == MAIN_USERNAME and password == MAIN_PASSWORD:
            st.session_state.authenticated = True
        else:
            st.error("Invalid credentials. Try again.")
else:
    # Machine Dashboard
    st.title("Machines Dashboard")
    
    for index, row in machine_data.iterrows():
        machine_id = row['Terminal']
        location = row['Location']
        status = "Down" if machine_id in down_machines else "Up"

        col1, col2, col3 = st.columns([1, 2, 2])
        with col1:
            st.image(
                "https://img.freepik.com/premium-photo/atm-machine-icon-banking-financial-services-symbol-art-logo-illustration_762678-19449.jpg?w=740",
                width=50,
            )
        with col2:
            st.markdown(f"**{location}**")
            st.markdown(f"ID: {machine_id}")
        with col3:
            st.markdown(f"Status: {status}")
            if st.button("View Details", key=f"details_{index}"):
                st.session_state.selected_machine = machine_id

    # Machine Details
    if "selected_machine" in st.session_state:
        machine_id = st.session_state.selected_machine
        st.header(f"Details for {machine_id}")
        machine = machine_data[machine_data['Terminal'] == machine_id].iloc[0]
        for col in machine.index:
            st.write(f"**{col}:** {machine[col]}")
        st.write("### Change Status")
        new_status = st.radio(
            "Select Status", ["Up", "Down"], index=1 if machine_id in down_machines else 0
        )
        status_password = st.text_input("Enter Password to Update Status", type="password")
        if st.button("Update Status"):
            if status_password == UPDATE_PASSWORD:
                if new_status == "Down":
                    down_machines.add(machine_id)
                else:
                    down_machines.discard(machine_id)
                st.success("Status updated successfully!")
            else:
                st.error("Incorrect password!")

        st.write("### Comments")
        if machine_id not in comments:
            comments[machine_id] = []
        for comment in comments[machine_id]:
            st.write(f"- {comment}")
        new_comment = st.text_area("Add a Comment")
        if st.button("Submit Comment"):
            comments[machine_id].append(new_comment)
            st.success("Comment added successfully!")
