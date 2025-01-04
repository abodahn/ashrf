import streamlit as st
import pandas as pd

# Hardcoded credentials
MAIN_USERNAME = 'admin'
MAIN_PASSWORD = '1234'
UPDATE_PASSWORD = '12'

# Example Excel file path (update this to your actual file path)
excel_path = 'D:\\New Microsoft Excel Worksheet.xlsx'

# Machines with a "down" status
down_machines = {'MOJ015', 'MOJ018', 'MOJ021', 'MOJ023', 'MOJ024'}

# Dictionary to store comments for each machine
comments = {}


# Load machine data from Excel
@st.cache_data
def load_machine_data():
    try:
        sheet_data = pd.read_excel(excel_path)
        return sheet_data
    except Exception as e:
        st.error(f"Error loading Excel file: {e}")
        return pd.DataFrame()


# Login page
def login():
    st.title("MOJ Project Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username == MAIN_USERNAME and password == MAIN_PASSWORD:
            st.session_state.logged_in = True
        else:
            st.error("Invalid credentials!")


# Dashboard page
def dashboard():
    st.title("Machines Dashboard")
    machine_data = load_machine_data()

    if machine_data.empty:
        st.error("No data available.")
        return

    # Display machine cards
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
            st.markdown(f"**Location:** {location}")
            st.markdown(f"**Terminal ID:** {machine_id}")
        with col3:
            st.markdown(f"**Status:** {status}")
            if st.button("View Details", key=f"details_{index}"):
                st.session_state.selected_machine = machine_id

    # Show machine details
    if "selected_machine" in st.session_state:
        show_machine_details(machine_data)


# Machine details page
def show_machine_details(machine_data):
    machine_id = st.session_state.selected_machine
    machine = machine_data[machine_data['Terminal'] == machine_id].iloc[0]

    st.header(f"Details for {machine_id}")
    for col in machine.index:
        st.write(f"**{col}:** {machine[col]}")

    # Update status
    st.subheader("Change Status")
    new_status = st.radio("Select Status", ["Up", "Down"], index=1 if machine_id in down_machines else 0)
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

    # Comments section
    st.subheader("Comments")
    if machine_id not in comments:
        comments[machine_id] = []
    for comment in comments[machine_id]:
        st.write(f"- {comment}")
    new_comment = st.text_area("Add a Comment")
    if st.button("Submit Comment"):
        comments[machine_id].append(new_comment)
        st.success("Comment added successfully!")


# Main function
def main():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        login()
    else:
        dashboard()


if __name__ == "__main__":
    main()
