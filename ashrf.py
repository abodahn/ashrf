import streamlit as st
import pandas as pd

# Hardcoded data for 28 machines
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
    # Add the remaining machines here...
]

# DataFrame and Down Machines
machine_data = pd.DataFrame(data)
down_machines = {"MOJ015", "MOJ018", "MOJ021", "MOJ023", "MOJ024"}
comments = {}

# Navigation State
if "page" not in st.session_state:
    st.session_state.page = "dashboard"
if "selected_machine" not in st.session_state:
    st.session_state.selected_machine = None

# Dashboard Page
if st.session_state.page == "dashboard":
    st.title("📊 Machines Dashboard")

    # Summary Metrics
    st.subheader("Overview")
    col1, col2, col3 = st.columns(3)
    total, up, down = len(machine_data), len(machine_data) - len(down_machines), len(down_machines)
    col1.metric("Total Machines", total)
    col2.metric("Up Machines", up, delta=f"+{up}")
    col3.metric("Down Machines", down, delta=f"-{down}", delta_color="inverse")

    # Search Bar
    st.subheader("Search Machines")
    search_query = st.text_input("Search by Location or Terminal:")
    if search_query:
        filtered_data = machine_data[
            machine_data['Location'].str.contains(search_query, case=False, na=False)
            | machine_data['Terminal'].str.contains(search_query, case=False, na=False)
        ]
    else:
        filtered_data = machine_data

    # Machines Grid
    st.subheader("Machine List")
    cols = st.columns(4)
    for index, row in filtered_data.iterrows():
        col = cols[index % 4]
        card_color = "#d4edda" if row["Terminal"] not in down_machines else "#f8d7da"
        border_color = "red" if row["Terminal"] in down_machines else "#ccc"
        with col:
            if st.button(f"View {row['Terminal']}", key=f"details_{row['Terminal']}"):
                st.session_state.page = "details"
                st.session_state.selected_machine = row["Terminal"]

# Details Page
if st.session_state.page == "details":
    selected_machine = st.session_state.selected_machine
    machine = machine_data[machine_data["Terminal"] == selected_machine].iloc[0]
    card_color = "#d4edda" if selected_machine not in down_machines else "#f8d7da"
    border_color = "red" if selected_machine in down_machines else "#ccc"

    st.title(f"Details for {selected_machine}")
    st.markdown(
        f"""
        <div style="border: 2px solid {border_color}; border-radius: 8px; padding: 20px; background-color: {card_color};">
            <strong>Location:</strong> {machine['Location']}<br>
            <strong>Terminal:</strong> {machine['Terminal']}<br>
            <strong>Status:</strong> {"Up" if selected_machine not in down_machines else "Down"}<br>
            <strong>First Operation:</strong> {machine['First Operation']}<br>
            <strong>Total Transactions:</strong> {machine['Total Transactions']}<br>
            <strong>Last CIT:</strong> {machine['Last CIT']}<br>
            <strong>No. Tickets:</strong> {machine['No. Tickets']}<br>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Comments Section
    st.subheader("Comments")
    new_comment = st.text_area("Add Comment")
    if st.button("Submit Comment"):
        comments[selected_machine] = comments.get(selected_machine, [])
        comments[selected_machine].append(new_comment)
        st.success("Comment added successfully!")

    for comment in comments.get(selected_machine, []):
        st.write(f"- {comment}")

    # Back to Dashboard
    if st.button("Back to Dashboard"):
        st.session_state.page = "dashboard"
