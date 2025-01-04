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
    # Add the rest of the data as per your requirement
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

    # Summary Section
    total_machines = len(machine_data)
    down_count = sum(machine_data['Terminal'].isin(down_machines))
    up_count = total_machines - down_count
    st.markdown(
        f"**Total Machines:** {total_machines} | **Up Machines:** {up_count} | **Down Machines:** {down_count}"
    )

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

        st.markdown(
            f"""
            <div style="border: 1px solid #ddd; border-radius: 10px; padding: 15px; margin: 10px; background-color: {card_color};">
                <h4>Location: {location}</h4>
                <p><strong>Terminal ID:</strong> {machine_id}</p>
                <p><strong>Status:</strong> {status}</p>
                <a href="#" style="text-decoration: none;">View Details</a>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Footer
    st.write("---")
    st.markdown("Powered by **MOJ Support System**")
