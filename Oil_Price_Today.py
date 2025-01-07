import streamlit as st
import requests
import json
import os

# API Details
API_URL = "https://api.oilpriceapi.com/v1/prices/latest"
API_KEY = "2cdd3408dc07625b07f0e294e2e9c1767be6363874694b89beccc6d8f14359e1"
PREVIOUS_PRICE_FILE = "previous_price.json"

# Function to fetch the latest oil price
def fetch_latest_oil_price():
    headers = {
        "Authorization": f"Token {API_KEY}",
        "Content-Type": "application/json",
    }
    response = requests.get(API_URL, headers=headers)
    if response.status_code == 200:
        return response.json().get("data", {})
    else:
        st.error(f"Failed to fetch data: {response.status_code} - {response.text}")
        return None

# Function to load the previous price
def load_previous_price():
    if os.path.exists(PREVIOUS_PRICE_FILE):
        with open(PREVIOUS_PRICE_FILE, "r") as file:
            return json.load(file).get("price", None)
    return None

# Function to save the latest price
def save_latest_price(price):
    with open(PREVIOUS_PRICE_FILE, "w") as file:
        json.dump({"price": price}, file)

# Streamlit App
st.title("Oil Price Notification Viewer")
st.write("This app retrieves the most recent oil price and alerts you for significant changes.")

# Fetch the latest oil price
latest_data = fetch_latest_oil_price()

if latest_data:
    # Extract price, currency, and timestamp
    price = float(latest_data.get("price", 0))
    timestamp = latest_data.get("timestamp")
    currency = latest_data.get("currency")

    # Display the latest price information
    st.subheader("Latest Oil Price Information")
    st.write(f"**Price:** {price} {currency}")
    st.write(f"**Timestamp:** {timestamp}")

    # Load the previous price
    previous_price = load_previous_price()

    # Check for significant change
    if previous_price:
        price_change = ((price - previous_price) / previous_price) * 100
        if abs(price_change) >= 5:  # Set threshold for significant change
            st.warning(f"Significant Price Change Detected: {price_change:.2f}%")
        else:
            st.info(f"Price Change: {price_change:.2f}% (within normal range)")
    else:
        st.info("No previous price found. This is the first recorded value.")

    # Save the latest price
    save_latest_price(price)

    # Display raw API data
    st.subheader("Raw API Response")
    st.json(latest_data)
else:
    st.error("No data available. Please check the API or your connection.")
