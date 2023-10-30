import streamlit as st


class ParkingLot:
    def __init__(self, capacity):
        self.capacity = capacity
        self.spots = [{"id": i, "name": None} for i in range(1, capacity + 1)]

    def check_in(self, spot_id, name):
        spot = next((spot for spot in self.spots if spot["id"] == spot_id), None)
        if spot and not spot["name"]:
            spot["name"] = name
            return True
        return False

    def check_out(self, spot_id):
        spot = next((spot for spot in self.spots if spot["id"] == spot_id), None)
        if spot and spot["name"]:
            spot["name"] = None
            return True
        return False

    def status(self):
        return self.spots


@st.cache(allow_output_mutation=True)
def get_parking_lot():
    return ParkingLot(10)


def main():
    st.title("Parking Lot Management System")

    parking_lot = get_parking_lot()

    with st.expander("Check In"):
        spot_id = st.number_input("Choose a parking spot (1-10) for Check In", min_value=1, max_value=10)
        name = st.text_input("Enter your name for Check In")
        if st.button("Check In"):
            if parking_lot.check_in(spot_id, name):
                st.success(f"Checked into parking spot {spot_id}.")
            else:
                st.error("Parking spot already taken!")

    with st.expander("Check Out"):
        spot_id = st.number_input("Choose your parking spot for Check Out", min_value=1, max_value=10)
        if st.button("Check Out from chosen spot"):
            if parking_lot.check_out(spot_id):
                st.success(f"Checked out from parking spot {spot_id}.")
            else:
                st.error("Parking spot is already vacant!")

    st.subheader("Parking Status")
    spots = parking_lot.status()
    for spot in spots:
        occupied = "Vacant"
        if spot["name"]:
            occupied = f"Occupied by {spot['name']}"
        st.write(f"Spot {spot['id']} - {occupied}")


if __name__ == "__main__":
    main()
