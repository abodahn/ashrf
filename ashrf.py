import streamlit as st
import pandas as pd

# Hardcoded credentials
MAIN_USERNAME = 'admin'
MAIN_PASSWORD = '1234'

# Hardcoded data for all 28 machines
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
    {"No.": 21, "Terminal": "MOJ021", "Location": "Suez", "First Operation": "2022-03-15", "Total Transactions": 1005, "Last CIT": "5 Feb 2024", "No. Tickets": 31},
    {"No.": 22, "Terminal": "MOJ022", "Location": "Fayoum", "First Operation": "2022-03-16", "Total Transactions": 1624, "Last CIT": "14 Aug 2024", "No. Tickets": 137},
    {"No.": 23, "Terminal": "MOJ023", "Location": "South Mansoura", "First Operation": "2022-03-17", "Total Transactions": 2273, "Last CIT": "21 Oct 2023", "No. Tickets": 11},
    {"No.": 24, "Terminal": "MOJ024", "Location": "North Zagazig", "First Operation": "2022-06-08", "Total Transactions": 1327, "Last CIT": "11 Nov 2023", "No. Tickets": 32},
    {"No.": 25, "Terminal": "MOJ025", "Location": "South Zagazig", "First Operation": "2022-07-08", "Total Transactions": 2135, "Last CIT": "29 May 2024", "No. Tickets": 89},
    {"No.": 26, "Terminal": "MOJ026", "Location": "Shebin El Koum", "First Operation": "2022-09-08", "Total Transactions": 1673, "Last CIT": "29 Sep 2024", "No. Tickets": 85},
    {"No.": 27, "Terminal": "MOJ027", "Location": "Marsa Matrouh", "First Operation": "2022-10-08", "Total Transactions": 2, "Last CIT": "6 Aug 2024", "No. Tickets": 7},
    {"No.": 28, "Terminal": "MOJ028", "Location": "North Mansoura", "First Operation": "2022-06-11", "Total Transactions": 75, "Last CIT": "28 Jan 2024", "No. Tickets": 11},
]

# DataFrame and Down Machines
machine_data = pd.DataFrame(data)
down_machines = {"MOJ015", "MOJ018", "MOJ021", "MOJ023", "MOJ024"}

# Comments dictionary
comments = {}

# Page Navigation
if "page" not in st.session_state:
    st.session_state.page = "dashboard"

if st.session_state.page == "dashboard":
    st.title("Machines Dashboard")
    total, up, down = len(machine_data), len(machine_data) - len(down_machines), len(down_machines)
    st.metric("Total Machines", total), st.metric("Up Machines", up), st.metric("Down Machines", down)
    for _, row in machine_data.iterrows():
        if st.button(f"View {row['Terminal']}", key=row['Terminal']):
            st.session_state.page, st.session_state.selected_machine = "details", row
elif st.session_state.page == "details":
    st.title(f"Details: {st.session_state.selected_machine['Terminal']}")
    st.write(st.session_state.selected_machine)
    st.button("Back", on_click=lambda: st.session_state.update({"page": "dashboard"}))
