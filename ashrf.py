import streamlit as st
import pandas as pd

# Hardcoded credentials
MAIN_USERNAME = 'admin'
MAIN_PASSWORD = '1234'
UPDATE_PASSWORD = '12'

# Hardcoded data (all machines added)
data = [
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
    # Add remaining machines here...
]

# Convert hardcoded data into a Pandas DataFrame
machine_data = pd.DataFrame(data)

# Machines with a "down" status
down_machines = {'MOJ015', 'MOJ018', 'MOJ021', 'MOJ023', 'MOJ024'}

# Dictionary to store comments for each machine
comments = {}

# Navigation Functionality
if "page" not in st.session_state:
    st.session_state.page = "dashboard"

# Page Navigation
if st.session_state.page == "dashboard":
    # Dashboard Page
    st.title("Machines Dashboard")

    # Summary Section
    st.subheader("Overview")
    total_machines = len(machine_data)
    down_count = sum(machine_data['Terminal'].isin(down_machines))
    up_count = total_machines - down_count
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Total Machines", value=total_machines)
    with col2:
        st.metric(label="Up Machines", value=up_count, delta=f"+{up_count}")
    with col3:
        st.metric(label="Down Machines", value=down_count, delta=f"-{down_count}", delta_color="inverse")

    # Search Bar
    st.subheader("Search Machines")
    search_query = st.text_input("Search by Location or Terminal:", placeholder="Enter location or terminal ID")
    if search_query:
        filtered_data = machine_data[
            machine_data['Location'].str.contains(search_query, case=False, na=False)
            | machine_data['Terminal'].str.contains(search_query, case=False, na=False)
        ]
    else:
        filtered_data = machine_data

    # Display Machines in Cards
    st.subheader("Machines List")
    for index, row in filtered_data.iterrows():
        machine_id = row['Terminal']
        location = row['Location']
        status = "Down" if machine_id in down_machines else "Up"
        card_color = "#d4edda" if status == "Up" else "#f8d7da"

        # Create a card for each machine
        if st.button(f"View Details for {machine_id}", key=f"details_{machine_id}"):
            st.session_state.page = "details"
            st.session_state.selected_machine = machine_id

elif st.session_state.page == "details":
    # Machine Details Page
    machine_id = st.session_state.selected_machine
    machine = machine_data[machine_data["Terminal"] == machine_id].iloc[0]
    st.title(f"Details for {machine_id}")

    # Display Machine Information
    st.subheader("Machine Information")
    for col, value in machine.items():
        st.write(f"**{col}:** {value}")

    # Add Comments Section
    st.subheader("Add Comments")
    new_comment = st.text_area(f"Add a Comment for {machine_id}")
    if st.button("Submit Comment"):
        comments[machine_id] = comments.get(machine_id, [])
        comments[machine_id].append(new_comment)
        st.success("Comment added successfully!")

    # Display Comments
    st.subheader("Comments")
    for comment in comments.get(machine_id, []):
        st.write(f"- {comment}")

    # Back Button
    if st.button("Back to Dashboard"):
        st.session_state.page = "dashboard"
