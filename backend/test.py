import requests
import os
from decouple import config

'''
api_key = config("POLYGON_API_KEY")
print("Api_key:",api_key)


symbol = 'AAPL'
#endpoint = f'https://api.polygon.io/v3/reference/options/contracts?underlying_symbol={symbol}&apiKey={api_key}'
endpoint = f'https://api.polygon.io/v3/reference/options/contracts?underlying_symbol={symbol}&perpage=50&page=1&apiKey={api_key}'
response = requests.get(endpoint)
if response.status_code != 200:
    raise Exception(f"Failed to fetch option chain data: {response.json()}")
data = response.json()
print("data", data)
if 'results' not in data or len(data['results']) == 0:
    raise Exception("No option chain data available for the given ticker.")

# Example of fetching strike prices and expiration dates
for option in data.get('results', []):
    print(f"Strike Price: {option['strike_price']} | Expiration: {option['expiration_date']}")
'''
import yfinance as yf

# Fetch the option chain for the ticker
ticker = yf.Ticker("AAPL")

# Step 1: Get available expiration dates
expirations = ticker.options
print("Available Expiration Dates:", expirations)

# Step 2: Select an expiration date and get the option chain
selected_expiration = expirations[0]  # Select the first available expiration
option_chain = ticker.option_chain(selected_expiration)

# Step 3: Get call options
calls = option_chain.calls
print(calls[['strike', 'lastPrice', 'impliedVolatility', 'openInterest', 'volume']])

# convert calls to dataframe and save as csv
calls_df = calls[['strike', 'lastPrice', 'impliedVolatility', 'openInterest', 'volume']]
calls_df.to_csv('calls.csv', index=False)
