from scipy.stats import norm
from scipy.optimize import toms748
import scipy.stats as si
import numpy as np

'''
def calc_implied_volatility(S,K,T,r,market_price, q):  

    def black_scholes_call(sigma):
        d1 = (np.log(S / K) + (r - q + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
        d2 = d1 - sigma * np.sqrt(T)
        BSprice_call=S * np.exp(-q * T) * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
        fx=BSprice_call-market_price
        return fx
    
    return optimize.brentq(black_scholes_call, 0.0001, 100, maxiter=1000)
'''

def calc_implied_volatility(S, K, T, r, market_price, q):
    def black_scholes_call(sigma):
        d1 = (np.log(S / K) + (r - q + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
        d2 = d1 - sigma * np.sqrt(T)
        BSprice_call = S * np.exp(-q * T) * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
        return BSprice_call - market_price  # The objective function

    # Debug: Evaluate the function at the initial bounds
    f_a = black_scholes_call(0.0001)
    f_b = black_scholes_call(100)
    print(f"f(0.0001) = {f_a}, f(100) = {f_b}, market_price = {market_price}")

    # Check if f(a) and f(b) have different signs
    if f_a * f_b > 0:
        print(f"No root found between bounds for strike {K} and market price {market_price}")
        return np.nan  # Return NaN to handle gracefully

    # Try to find the root using Brent's method
    #return optimize.brentq(black_scholes_call, 0.0001, 100, maxiter=1000)
    return toms748(black_scholes_call, 0.0001, 100)

# Example Usage  
#print(calc_implied_volatility(S=8,K=6,T=0.25, r=0, market_price=4, q = 0.25))
