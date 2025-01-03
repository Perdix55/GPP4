import requests
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# API Endpoint and Key
HISTORICAL_API_URL = "https://api.oilpriceapi.com/v1/prices"
API_KEY = "2cdd3408dc07625b07f0e294e2e9c1767be6363874694b89beccc6d8f14359e1"

# Function to fetch historical oil prices
def fetch_historical_oil_prices(api_url, api_key):
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    response = requests.get(api_url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return pd.DataFrame(data.get("data", []))
    else:
        st.error(f"Failed to fetch data: {response.status_code} - {response.text}")
        return pd.DataFrame()

# Streamlit App
st.title("Oil Price Trends and Analysis")
st.write("This app retrieves historical oil price data and visualizes it.")

# Fetch historical data
st.subheader("Fetching Historical Data...")
data = fetch_historical_oil_prices(HISTORICAL_API_URL, API_KEY)

if not data.empty:
    # Process the data
    data["date"] = pd.to_datetime(data["time"])  # Convert timestamp to datetime
    data["price"] = data["price"].astype(float)
    data = data.sort_values("date")  # Sort data by date

    # Display raw data
    st.write(f"### Total Records Retrieved: {len(data)}")
    st.write("#### Sample Data:")
    st.write(data[["date", "price"]].head())

    # Visualization: Line Chart of Oil Prices
    st.subheader("Oil Price Trends Over Time")
    plt.figure(figsize=(10, 5))
    plt.plot(data["date"], data["price"], marker="o", label="Oil Prices (USD)")
    plt.title("Historical Oil Prices")
    plt.xlabel("Date")
    plt.ylabel("Price (USD per Barrel)")
    plt.grid()
    plt.legend()
    st.pyplot(plt)

    # Insights
    st.subheader("Insights and Trends")
    st.write(f"Most Recent Price: ${data['price'].iloc[-1]:.2f} on {data['date'].iloc[-1].strftime('%Y-%m-%d')}")
    st.write(f"Oldest Price: ${data
