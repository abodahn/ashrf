import streamlit as st
import pandas as pd

# Hardcoded data for machines
data = [
    {"No.": 1, "Terminal": "MOJ001", "Location": "Heliopolis", "First Operation": "2021-09-26", "Total Transactions": 0, "Last CIT": "19 Sep 2024", "No. Tickets": 109},
    {"No.": 2, "Terminal": "MOJ002", "Location": "South Cairo", "First Operation": "2021-05-05", "Total Transactions": 1634, "Last CIT": "23 Jul 2024", "No. Tickets": 66},
    {"No.": 3, "Terminal": "MOJ003", "Location": "North Cairo", "First Operation": "2021-05-20", "Total Transactions": 8876, "Last CIT": "19 Aug 2024", "No. Tickets": 43},
    {"No.": 4, "Terminal": "MOJ004", "Location": "East Alex", "First Operation": "2021-06-26", "Total Transactions": 0, "Last CIT": "16 Sep 2024", "No. Tickets": 91},
    {"No.": 5, "Terminal": "MOJ005", "Location": "West Alex", "First Operation": "2021-06-21", "Total Transactions": 244, "Last CIT": "10 Feb 2024", "No. Tickets": 44},
]

# DataFrame and Down Machines
machine_data = pd.DataFrame(data)
down_machines = {"MOJ003", "MOJ004", "MOJ005"}
comments = {}

# Initialize session state for navigation and selection
if "page" not in st.session_state:
    st.session_state.page = "dashboard"
if "selected_machine" not in st.session_state:
    st.session_state.selected_machine = None


def show_dashboard():
    """Display the dashboard page."""
    st.title("📊 Machines Dashboard")

    # Overview metrics
    st.subheader("Overview")
    col1, col2, col3 = st.columns(3)
    total_machines = len(machine_data)
    down_count = len([m for m in machine_data["Terminal"] if m in down_machines])
    up_count = total_machines - down_count
    col1.metric("Total Machines", total_machines)
    col2.metric("Up Machines", up_count)
    col3.metric("Down Machines", down_count)

    # Bar chart for distribution
    st.subheader("Machine Status Distribution")
    status_data = pd.DataFrame(
        {"Status": ["Up", "Down"], "Count": [up_count, down_count]}
    )
    st.bar_chart(status_data.set_index("Status"))

    # Search functionality
    st.subheader("Search Machines")
    search_query = st.text_input("Search by Location or Terminal:")
    if search_query:
        filtered_data = machine_data[
            machine_data["Location"].str.contains(search_query, case=False, na=False)
            | machine_data["Terminal"].str.contains(search_query, case=False, na=False)
        ]
    else:
        filtered_data = machine_data

    # Machine list grid
    st.subheader("Machine List")
    cols = st.columns(2)
    for index, row in filtered_data.iterrows():
        col = cols[index % 2]
        status_color = "green" if row["Terminal"] not in down_machines else "red"
        with col:
            if st.button(f"View Details: {row['Terminal']}", key=f"view_{row['Terminal']}"):
                st.session_state.page = "details"
                st.session_state.selected_machine = row["Terminal"]
                st.experimental_rerun()


def show_details():
    """Display the details page for the selected machine."""
    selected_machine = st.session_state.selected_machine
    machine = machine_data[machine_data["Terminal"] == selected_machine].iloc[0]

    st.title(f"Details for {selected_machine}")

    # Machine details
    st.subheader("Machine Information")
    for key, value in machine.items():
        st.write(f"**{key}:** {value}")

    # Change status
    st.subheader("Update Status")
    current_status = "Down" if selected_machine in down_machines else "Up"
    new_status = st.radio("Change Status", ["Up", "Down"], index=0 if current_status == "Up" else 1)
    if st.button("Update Status"):
        if new_status == "Down":
            down_machines.add(selected_machine)
        else:
            down_machines.discard(selected_machine)
        st.success("Status updated successfully!")

    # Comments section
    st.subheader("Comments")
    new_comment = st.text_area("Add Comment")
    if st.button("Submit Comment"):
        comments[selected_machine] = comments.get(selected_machine, [])
        comments[selected_machine].append(new_comment)
        st.success("Comment added successfully!")

    for comment in comments.get(selected_machine, []):
        st.write(f"- {comment}")

    # Back to dashboard
    if st.button("Back to Dashboard"):
        st.session_state.page = "dashboard"
        st.experimental_rerun()


# Routing
if st.session_state.page == "dashboard":
    show_dashboard()
elif st.session_state.page == "details":
    show_details()
