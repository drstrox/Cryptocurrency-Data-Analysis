# -*- coding: utf-8 -*-
"""Cryptocurrency.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1EmLRRKzzxHTlYPN7miCnQkiClphGKmAc
"""

import requests
import pandas as pd

# Function to fetch top 50 cryptocurrencies data
def fetch_crypto_data():
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": 50,  # Fetch top 50 cryptocurrencies
        "page": 1
    }
    response = requests.get(url, params=params)
    data = response.json()

    # Extract relevant data
    crypto_data = []
    for coin in data:
        crypto_data.append({
            "Name": coin["name"],
            "Symbol": coin["symbol"],
            "Current Price (USD)": coin["current_price"],
            "Market Capitalization (USD)": coin["market_cap"],
            "24h Trading Volume (USD)": coin["total_volume"],
            "Price Change (24h, %)": coin["price_change_percentage_24h"]
        })

    # Convert data to a DataFrame for easy analysis
    df = pd.DataFrame(crypto_data)
    return df

# Fetch the top 50 cryptocurrencies data
crypto_df = fetch_crypto_data()

# Display the top 50 cryptocurrencies
print(crypto_df)

# Analyze the data
def analyze_data(df):
    # Top 5 cryptocurrencies by market capitalization
    top_5 = df.sort_values(by="Market Capitalization (USD)", ascending=False).head(5)

    # Average price of top 50 cryptocurrencies
    avg_price = df["Current Price (USD)"].mean()

    # Highest and lowest 24h price change percentage
    highest_change = df.loc[df["Price Change (24h, %)"].idxmax()]
    lowest_change = df.loc[df["Price Change (24h, %)"].idxmin()]

    return top_5, avg_price, highest_change, lowest_change

# Perform analysis
top_5, avg_price, highest_change, lowest_change = analyze_data(crypto_df)

# Print analysis results
print("Top 5 Cryptocurrencies by Market Cap:")
print(top_5)

print(f"\nAverage Price of Top 50 Cryptocurrencies: ${avg_price:.2f}")

print(f"\nHighest 24h Price Change: {highest_change['Name']} ({highest_change['Price Change (24h, %)']}%)")
print(f"Lowest 24h Price Change: {lowest_change['Name']} ({lowest_change['Price Change (24h, %)']}%)")

import requests
import openpyxl
import time


def write_to_excel(df, filename="crypto_data.xlsx"):
    # Create a new workbook or open an existing one
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Crypto Data"

    # Write header row
    headers = df.columns.tolist()
    ws.append(headers)

    # Write data rows
    for row in df.itertuples(index=False, name=None):
        ws.append(row)

    # Save the workbook
    wb.save(filename)

# Continuously update the data every 5 minutes
while True:
    crypto_df = fetch_crypto_data()  # Fetch new data
    write_to_excel(crypto_df)  # Write the data to Excel
    print("Excel sheet updated.")
    time.sleep(300)  # Wait for 5 minutes before fetching new data