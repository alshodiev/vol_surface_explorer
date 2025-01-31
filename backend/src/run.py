'import requests
from fetch_data import get_option_chain
from black_scholes import calc_implied_volatility
from scipy.optimize import brentq
import numpy as np
from flask import Flask, request, jsonify
from flask_cors import CORS
# Venv for this project is called vol_explorer
    
app = Flask(__name__)
CORS(app)

@app.route('/calculate_iv_surface', methods=['POST'])
def calculate_iv_surface():
    try:
        # Parse input from Streamlit requiest
        data = request.json
        ticker = data['ticker']
        rf_rate = data['rf_rate']
        div_yield = data['div_yield']
        min_strike_pct = data['min_strike_pct']
        max_strike_pct = data['max_strike_pct']
        expiry_range = data['expiry_range']

        # Fetch option data
        options = get_option_chain(ticker, min_strike_pct, max_strike_pct, expiry_range)

        spot_price = options['spot']
        results = []

        for call in options['calls']:
            iv = calc_implied_volatility(
                S=spot_price,
                K=call['strike'],
                T=call['expiry'],
                r=rf_rate,
                market_price=call['market_price'],
                q=div_yield
            )
            if not np.isnan(iv):  # Skip invalid IVs            
                results.append({
                    'type' :'call',
                    'strike': call['strike'],
                    'expiry': call['expiry'],
                    'market_price' : call['market_price'],
                    'iv': iv
                })
        for put in options['puts']:
            iv = calc_implied_volatility(
                S=spot_price,
                K=put['strike'],
                T=put['expiry'],
                r=rf_rate,
                market_price=put['market_price'],
                q=div_yield
            )
            if not np.isnan(iv):  # Skip invalid IVs
                results.append({
                    'type' :'put',
                    'strike': put['strike'],
                    'expiry': put['expiry'],
                    'market_price' : put['market_price'],
                    'iv': iv
                })
        print("Jsonified results", jsonify(results))
        return jsonify(results)
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)})


if __name__ == '__main__':
    app.run(port = 5000)

#if __name__ == '__main__':
#    results = calculate_iv_surface("AAPL", 0.8, 1.2, 0.03, 0.01, (1.5, 2))
#    for res in results[:5]:
#        print(f"Strike: {res['strike']}, Expiry: {res['expiry']}, IV: {res['iv']:.4f}, Market Price: {res['market_price']}")
