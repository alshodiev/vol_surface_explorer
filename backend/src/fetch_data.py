import yfinance as yf
from datetime import datetime

def get_spot_price(ticker):
    """
    Fetches the spot price of the given ticker using yfinance.
    """
    stock = yf.Ticker(ticker)
    spot_price = stock.history(period="1d")['Close'].iloc[-1]
    return float(spot_price)

def get_option_chain(ticker, min_strike_pct, max_strike_pct, expiry_range):
    """
    Fetches the option chain using yfinance and filters options based on the given strike price 
    and time-to-expiry criteria.
    """
    stock = yf.Ticker(ticker)

    # Get available expiration dates
    expirations = stock.options
    filtered_calls = []
    filtered_puts = []

    # Get the spot price
    spot_price = get_spot_price(ticker)
    min_strike = min_strike_pct * spot_price
    max_strike = max_strike_pct * spot_price

    # Loop through expiration dates
    for expiration_date in expirations:
        # Calculate time to expiry
        time_to_expiry = max((datetime.strptime(expiration_date, "%Y-%m-%d") - datetime.now()).days / 365.0, 0.01)

        # Skip expiration dates outside the desired expiry range
        if not (expiry_range[0] <= time_to_expiry <= expiry_range[1]):
            continue

        # Get option chain for the specific expiration date
        option_chain = stock.option_chain(expiration_date)
        calls = option_chain.calls
        puts = option_chain.puts

        # Filter calls
        for _, row in calls.iterrows():
            strike_price = row['strike']
            if min_strike <= strike_price <= max_strike:
                filtered_calls.append({
                    'strike': strike_price,
                    'expiry': time_to_expiry,
                    'market_price': row['lastPrice']
                })

        # Filter puts
        for _, row in puts.iterrows():
            strike_price = row['strike']
            if min_strike <= strike_price <= max_strike:
                filtered_puts.append({
                    'strike': strike_price,
                    'expiry': time_to_expiry,
                    'market_price': row['lastPrice']
                })

    return {
        'spot': spot_price,
        'calls': filtered_calls,
        'puts': filtered_puts
    }

