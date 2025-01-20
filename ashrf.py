import streamlit as st
import math
import pandas as pd
import requests

# Fleet data
fleet = [
    {"number_plate": "ABC123", "current_km": 12000, "fuel_efficiency": 15, "history": []},
    {"number_plate": "XYZ789", "current_km": 8500, "fuel_efficiency": 12, "history": []},
    {"number_plate": "LMN456", "current_km": 15000, "fuel_efficiency": 10, "history": []},
    {"number_plate": "PQR321", "current_km": 7000, "fuel_efficiency": 14, "history": []},
]

# Driver data
drivers = {"John Doe": [], "Jane Smith": []}

# Photon API endpoint
PHOTON_API_URL = "https://photon.komoot.io/api/"


def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Radius of the Earth in km
    d_lat = math.radians(lat2 - lat1)
    d_lon = math.radians(lon2 - lon1)
    a = math.sin(d_lat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(d_lon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c


def resolve_place_to_coords(place_name):
    if not place_name or len(place_name.strip()) == 0:
        return None
    params = {"q": place_name}
    response = requests.get(PHOTON_API_URL, params=params)
    if response.status_code == 200:
        try:
            results = response.json()
            if results["features"]:
                coords = results["features"][0]["geometry"]["coordinates"]
                return float(coords[1]), float(coords[0])  # Photon returns [lon, lat]
        except (requests.exceptions.JSONDecodeError, KeyError):
            pass
    return None


# Streamlit app
st.title("Fleet Manager")

# Input form
with st.form("add_trip_form"):
    st.subheader("Add a Trip")
    number_plate = st.selectbox("Select Number Plate", [car["number_plate"] for car in fleet])
    start_location = st.text_input("Start Location")
    end_location = st.text_input("End Location")
    driver_name = st.selectbox("Select Driver", list(drivers.keys()))
    submitted = st.form_submit_button("Add Move")

if submitted:
    start_coords = resolve_place_to_coords(start_location)
    end_coords = resolve_place_to_coords(end_location)

    if not start_coords or not end_coords:
        st.error("Invalid locations. Please check your input.")
    else:
        start_lat, start_lon = start_coords
        end_lat, end_lon = end_coords

        # Calculate distance
        distance = haversine(start_lat, start_lon, end_lat, end_lon)

        # Find the car
        for car in fleet:
            if car["number_plate"] == number_plate:
                car["history"].insert(0, {
                    "start": start_location,
                    "end": end_location,
                    "distance": round(distance, 2),
                    "driver": driver_name
                })
                car["current_km"] += round(distance, 2)
                car["history"] = car["history"][:10]  # Keep last 10 moves

                # Fuel cost calculation
                fuel_cost = (distance / car["fuel_efficiency"]) * 3.5  # Example fuel price
                if driver_name in drivers:
                    drivers[driver_name].append({
                        "number_plate": number_plate,
                        "route": f"{start_location} → {end_location}",
                        "distance": round(distance, 2),
                        "fuel_cost": round(fuel_cost, 2)
                    })

                st.success(f"Trip added for {number_plate}.")

# Dashboard
st.subheader("Dashboard")
total_distance_today = sum([trip["distance"] for driver in drivers.values() for trip in driver])
top_driver = max(drivers.items(), key=lambda x: sum([trip["distance"] for trip in x[1]]), default=None)

st.metric("Total Distance Today", f"{total_distance_today:.2f} km")
st.metric("Top Driver", top_driver[0] if top_driver else "None")

# Fleet details
st.subheader("Fleet Details")
for car in fleet:
    st.write(f"**Number Plate:** {car['number_plate']}")
    st.write(f"**Current KM:** {car['current_km']}")
    st.write("**Last 10 Moves:**")
    if car["history"]:
        for move in car["history"]:
            st.write(f"{move['start']} → {move['end']} ({move['distance']} km)")
    else:
        st.write("No moves recorded.")

# Export history
if st.button("Export Trip History"):
    data = []
    for car in fleet:
        for move in car["history"]:
            data.append({
                "Number Plate": car["number_plate"],
                "Driver": move.get("driver"),
                "Start": move["start"],
                "End": move["end"],
                "Distance (km)": move["distance"]
            })

    df = pd.DataFrame(data)
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("Download CSV", data=csv, file_name="trip_history.csv", mime="text/csv")
