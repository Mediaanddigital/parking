import streamlit as st
import json
from datetime import datetime

DATA_FILE = 'parking_data.json'

# Default parking data
def default_data():
    # Initialize all spots as None (vacant)
    return [{"id": i, "name": None} for i in range(1, 13)]

# Read parking data from the file or initialize if file doesn't exist
def read_data():
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        # File doesn't exist, return default data
        return default_data()

# Save parking data to the file
def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f)

def check_in(spots, spot_id, name):
    spot = next((spot for spot in spots if spot["id"] == spot_id), None)
    if spot and not spot["name"]:
        spot["name"] = name
        return True
    return False

def check_out(spots, spot_id):
    spot = next((spot for spot in spots if spot["id"] == spot_id), None)
    if spot and spot["name"]:
        spot["name"] = None
        return True
    return False

def reset_required():
    now = datetime.now()
    if now.weekday() == 2 and now.hour == 7 and now.minute == 30:
        return True
    return False

def main():
    st.title("🅿️ Parking Lot Management System")

    # Check if reset is required (Every Wednesday at 7:30)
    if reset_required():
        spots = default_data()
        save_data(spots)
    else:
        spots = read_data()

    with st.expander("Check In"):
        spot_id = st.number_input("Choose a parking spot (1-12) for Check In", min_value=1, max_value=12, value=1, step=1)
        name = st.text_input("Enter your name for Check In")
        if st.button("Check In"):
            if check_in(spots, spot_id, name):
                st.success(f"Checked into parking spot {spot_id}.")
                save_data(spots)
            else:
                st.error("Parking spot already taken or invalid name!")

    with st.expander("Check Out"):
        spot_id = st.number_input("Choose your parking spot (1-12) for Check Out", min_value=1, max_value=12, value=1, step=1)
        if st.button("Check Out from chosen spot"):
            if check_out(spots, spot_id):
                st.success(f"Checked out from parking spot {spot_id}.")
                save_data(spots)
            else:
                st.error("Parking spot is already vacant!")

    st.subheader("Parking Status")
    for spot in spots:
        status = "Vacant" if spot["name"] is None else f"Occupied by {spot['name']}"
        st.write(f"Spot {spot['id']} - {status}")

if __name__ == "__main__":
    main()
