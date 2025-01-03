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
if os.path.exists(CACHE
