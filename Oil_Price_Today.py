import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt

# API Details
API_URL = "https://api.oilpriceapi.com/v1/prices/by-period"
API_KEY = "2cdd3408dc07625b07f0e294e2e9c1767be6363874694b89beccc6d8f14359e1"

# Function to fetch historical oil prices
def fetch_historical_oil_prices(start_date, end_date):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }
    params = {
        "start": start_date,
        "end": end_date,
    }
    response = requests.get(API_URL, headers=headers, params=params)
    if response.status_code == 200:
        return pd.DataFrame(response.json().get("data", []))
    else:
        st.error(f"Error fetching data: {response.status_code} - {response.text}")
        return pd.DataFrame()

# Streamlit App
st.title("Historical Oil Price Viewer")
st.write("View oil price data for a custom date range using the Oil Price API.")

# Sidebar Input for Date Range
st.sidebar.header("Input Date Range")
start_date = st.sidebar.date_input("Start Date", value=pd.Timestamp("2023-01-01"))
end_date = st.sidebar.date_input("End Date", value=pd.Timestamp("2023-12-31"))

if start_date > end_date:
    st.sidebar.error("Start Date must be before End Date.")

# Fetch and display data
if st.sidebar.button("Fetch Data"):
    st.subheader("Fetching Data...")
    data = fetch_historical_oil_prices(start_date.isoformat(), end_date.isoformat())

    if not data.empty:
        # Process the data
        data["time"] = pd.to_datetime(data["time"])
        data["price"] = data["price"].astype(float)

        # Display Data
        st.write(f"### Data from {start_date} to {end_date}")
        st.write(data.head())

        # Visualization
        st.subheader("Oil Price Trends")
        plt.figure(figsize=(10, 6))
        plt.plot(data["time"], data["price"], marker="o", label="Oil Prices (USD)")
        plt.title("Oil Price Trends")
        plt.xlabel("Date")
        plt.ylabel("Price (USD per Barrel)")
        plt.grid()
        plt.legend()
        st.pyplot(plt)
    else:
        st.error("No data available for the selected date range.")
