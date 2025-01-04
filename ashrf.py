import streamlit as st
import pandas as pd

# Hardcoded credentials
MAIN_USERNAME = 'admin'
MAIN_PASSWORD = '1234'
UPDATE_PASSWORD = '12'

# Hardcoded data (all data added)
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
    {"No.": 12, "Terminal": "MOJ012", "Location": "Sharm El Sheikh", "First Operation": "2022-02-03", "Total Transactions": 554, "Last CIT": "7 Aug 2024", "No. Tickets": 16},
    {"No.": 13, "Terminal": "MOJ013", "Location": "City Stars", "First Operation": "2021-12-20", "Total Transactions": 45, "Last CIT": "3 Apr 2024", "No. Tickets": 14},
    {"No.": 14, "Terminal": "MOJ014", "Location": "Bank Misr Mohamed Farid", "First Operation": "2022-09-02", "Total Transactions": 46, "Last CIT": "28 Feb 2024", "No. Tickets": 5},
    {"No.": 15, "Terminal": "MOJ015", "Location": "Hurghada", "First Operation": "2022-02-13", "Total Transactions": 285, "Last CIT": "17 Jan 2024", "No. Tickets": 16},
    {"No.": 16, "Terminal": "MOJ016", "Location": "Luxor", "First Operation": "2022-02-14", "Total Transactions": 6, "Last CIT": "7 Jul 2024", "No. Tickets": 9},
    {"No.": 17, "Terminal": "MOJ017", "Location": "Sohag", "First Operation": "2022-02-15", "Total Transactions": 19181, "Last CIT": "28 Aug 2024", "No. Tickets": 154},
    {"No.": 18, "Terminal": "MOJ018", "Location": "Al Minya", "First Operation": "2022-02-17", "Total Transactions": 6375, "Last CIT": "29 Aug 2024", "No. Tickets": 145},
    {"No.": 19, "Terminal": "MOJ019", "Location": "PortSaid", "First Operation": "2022-03-13", "Total Transactions": 1743, "Last CIT": "24 Mar 2024", "No. Tickets": 27},
    {"No.": 20, "Terminal": "MOJ020", "Location": "Ismaillia", "First Operation": "2022-03-14", "Total Transactions": 475, "Last CIT": "12 Aug 2024", "No. Tickets": 61},
    # Continue adding the rest of the data here...
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

    # Search Bar
    search_query = st.text_input("Search by Location or Terminal:")
    if search_query:
        filtered_data = machine_data[
            machine_data['Location'].str.contains(search_query, case=False, na=False)
            | machine_data['Terminal'].str.contains(search_query, case=False, na=False)
        ]
    else:
        filtered_data = machine_data

    # Display Machines
    for index, row in filtered_data.iterrows():
        machine_id = row['Terminal']
        location = row['Location']
        status = "Down" if machine_id in down_machines else "Up"
        card_color = "lightgreen" if status == "Up" else "salmon"

        if st.button(f"View Details: {machine_id}"):
            st.session_state.selected_machine = machine_id

    # Machine Details Section
    if "selected_machine" in st.session_state:
        machine_id = st.session_state.selected_machine
        machine = machine_data[machine_data["Terminal"] == machine_id].iloc[0]
        st.markdown(f"### Details for {machine_id}")
        for col, value in machine.items():
            st.write(f"**{col}:** {value}")
        new_comment = st.text_area(f"Add Comment for {machine_id}")
        if st.button(f"Submit Comment for {machine_id}"):
            comments[machine_id] = comments.get(machine_id, [])
            comments[machine_id].append(new_comment)
            st.success("Comment added successfully!")
        st.markdown("### Comments")
        for comment in comments.get(machine_id, []):
            st.write(f"- {comment}")
