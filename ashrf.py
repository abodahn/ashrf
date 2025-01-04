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
    # Add remaining machines here...
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
    st.title("MOJ Machine Monitoring System")
    username = st.text_input("Username", placeholder="Enter username")
    password = st.text_input("Password", type="password", placeholder="Enter password")
    if st.button("Login"):
        if username == MAIN_USERNAME and password == MAIN_PASSWORD:
            st.session_state.authenticated = True
        else:
            st.error("Invalid credentials. Please try again.")
else:
    # Main Dashboard
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
        st.markdown(
            f"""
            <div style="border: 1px solid #ddd; border-radius: 10px; padding: 15px; margin: 10px 0; background-color: {card_color};">
                <h4 style="margin: 0;">{location}</h4>
                <p style="margin: 5px 0;"><strong>Terminal ID:</strong> {machine_id}</p>
                <p style="margin: 5px 0;"><strong>Status:</strong> {status}</p>
                <a href="?selected_machine={machine_id}" style="text-decoration: none; color: #007bff;">View Details</a>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Machine Details Section
    selected_machine = st.experimental_get_query_params().get("selected_machine", [None])[0]
    if selected_machine:
        machine = machine_data[machine_data["Terminal"] == selected_machine].iloc[0]
        st.subheader(f"Details for {selected_machine}")
        st.write("### Machine Information")
        for col, value in machine.items():
            st.write(f"**{col}:** {value}")
        st.write("### Add Comments")
        new_comment = st.text_area(f"Add Comment for {selected_machine}")
        if st.button(f"Submit Comment for {selected_machine}"):
            comments[selected_machine] = comments.get(selected_machine, [])
            comments[selected_machine].append(new_comment)
            st.success("Comment added successfully!")
        st.write("### Comments")
        for comment in comments.get(selected_machine, []):
            st.write(f"- {comment}")
