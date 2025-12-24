import streamlit as st
import requests

# ---------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------
st.set_page_config(
    page_title="Smart Train Selector (API)",
    page_icon="🚆",
    layout="centered"
)

st.title("🚆 Smart Train Selector (API Based)")
st.write("Live train status using IRCTC API")

# ---------------------------------------------------------
# API CONFIG (USE STREAMLIT SECRETS)
# ---------------------------------------------------------
RAPIDAPI_KEY = st.secrets["34556d9462msh33dac86393efc71p1d1a90jsnda9e34a609f8"]

API_URL = "https://irctc1.p.rapidapi.com/api/v1/getLiveTrainStatus"

HEADERS = {
    "X-RapidAPI-Key": RAPIDAPI_KEY,
    "X-RapidAPI-Host": "irctc1.p.rapidapi.com"
}

# ---------------------------------------------------------
# FUNCTION: CALL API
# ---------------------------------------------------------
def get_live_train_status(train_no):
    params = {"trainNo": train_no}
    response = requests.get(API_URL, headers=HEADERS, params=params, timeout=10)

    if response.status_code != 200:
        return None

    return response.json()

# ---------------------------------------------------------
# UI
# ---------------------------------------------------------
train_no = st.text_input("Enter Train Number", placeholder="e.g. 12951")

if st.button("Get Live Train Status"):
    if not train_no.strip():
        st.warning("Please enter a train number")
    else:
        with st.spinner("Fetching live train status..."):
            data = get_live_train_status(train_no)

        if not data or "data" not in data:
            st.error("Failed to fetch train status. Try again.")
        else:
            info = data["data"]

            st.success(f"🚆 {info.get('train_name', 'Train')} ({train_no})")

            col1, col2 = st.columns(2)

            with col1:
                st.metric("Current Station", info.get("current_station_name", "N/A"))
                st.metric("Last Updated", info.get("last_updated", "N/A"))

            with col2:
                st.metric("Delay (min)", info.get("delay", "N/A"))
                st.metric("Next Station", info.get("next_station_name", "N/A"))

            st.subheader("Full API Response")
            st.json(data)
