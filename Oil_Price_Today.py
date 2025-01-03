import requests
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from datetime import datetime
import pytz
import schedule
import time
import os

# API Endpoint and Key
HISTORICAL_API_URL = "https://api.oilpriceapi.com/v1/prices"
API_KEY = "2cdd3408dc07625b07f0e294e2e9c1767be6363874694b89beccc6d8f14359e1"
CACHE_FILE = "historical_oil_prices.csv"

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

# Function to save fetched data locally
def save_historical_data():
    data = fetch_historical_oil_prices(HISTORICAL_API_URL, API_KEY)
    if not data.empty:
        data.to_csv(CACHE_FILE, index=False)
        print("Data saved successfully.")

# Schedule the task to run daily at 8:00 AM EST
def schedule_daily_check():
    est = pytz.timezone("US/Eastern")
    now = datetime.now(tz=est)
    print(f"Scheduler running at {now.strftime('%Y-%m-%d %H:%M:%S')} EST")
schedule.every().day.at("08:00").do(save_historical_data)

# Fetch or load historical data
if os.path.exists(CACHE_FILE):
    data = pd.read_csv(CACHE_FILE)
else:
    data = pd.DataFrame()
    st.error("No cached data found. Please wait until the next scheduled update.")

# Streamlit App
st.title("Oil Price Trends and Analysis")
st.write("This app retrieves historical oil price data and visualizes it.")

if not data.empty:
    # Process the data
    data["date"] = pd.to_datetime(data["time"])
    data["price"] = data["price"].astype(float)
    data = data.sort_values("date")

    # Visualization
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
    st.write(f"Oldest Price: ${data['price'].iloc[0]:.2f} on {data['date'].iloc[0].strftime('%Y-%m-%d')}")
    if data["price"].iloc[-1] > data["price"].iloc[-2]:
        st.write("Oil prices have increased in the most recent period.")
    else:
        st.write("Oil prices have decreased in the most recent period.")

else:
    st.error("No historical data available to visualize.")

# Run the scheduler in the background
while True:
    schedule.run_pending()
    time.sleep(1)
