import streamlit as st
import requests
import pandas as pd
import numpy as np
import plotly.graph_objects as go

st.title("Volatility Surface Explorer")

# User inputs
calls_or_puts = st.radio("Select Calls or Puts", ["Calls", "Puts"])
ticker = st.text_input("Enter the Ticker Symbol", value="AAPL")
min_strike = st.slider("Minimum Strike Price % of Spot", 50, 100, 80)
max_strike = st.slider("Maximum Strike Price % of Spot", 100, 150, 120)
expiry_range = st.slider("Expiry Range (in years)", 0.0, 2.0, (0.0, 1.5))
risk_free_rate = st.number_input("Risk-Free Rate")
dividend_yield = st.number_input("Dividend Yield")

if st.button("Calculate IV Surface"):
    # Call backend API (assuming it's running locally on port 5000)
    backend_url = f"http://127.0.0.1:5000/calculate_iv_surface"
    response = requests.post(backend_url, json={
        "ticker": ticker,
        "rf_rate": risk_free_rate,
        "div_yield": dividend_yield,
        "min_strike_pct": min_strike / 100,
        "max_strike_pct": max_strike / 100,
        "expiry_range": expiry_range
    })

    if response.status_code == 200:
        data = response.json()
        df = pd.DataFrame(data)

        # Show raw data
        st.write("Calculated IV Surface Data:")
        #st.dataframe(df)
        
        df = df.sort_values(by=['expiry', 'strike'])
        df['iv'] = df['iv'].interpolate(method='linear', axis=0).fillna(method='bfill').fillna(method='ffill')
        st.dataframe(df)
        
        calls_df = df[df['type'] == 'call']
        calls_df = calls_df[calls_df['iv'] <= 60]
        puts_df = df[df['type'] == 'put']

        # Pivot the data to create a grid for surface plotting

        # Pivot for calls
        calls_iv_grid = calls_df.pivot_table(index='strike', columns='expiry', values='iv').values
        calls_expiry_grid, calls_strike_grid = np.meshgrid(
            calls_df['expiry'].unique(), calls_df['strike'].unique()
        )

        # Pivot for puts
        puts_iv_grid = puts_df.pivot_table(index='strike', columns='expiry', values='iv').values
        puts_expiry_grid, puts_strike_grid = np.meshgrid(
            puts_df['expiry'].unique(), puts_df['strike'].unique()
        )

        st.write("Rows with High IV:")
        st.dataframe(calls_df[calls_df['iv'] > 60])


        # Plot IV surface
        if calls_or_puts == "Calls":
            fig = go.Figure(data=[go.Surface(
                z=calls_iv_grid,
                x=calls_expiry_grid,
                y=calls_strike_grid,
                colorscale='Viridis'
            )])
        else:
            fig = go.Figure(data=[go.Surface(
                z=puts_iv_grid,
                x=puts_expiry_grid,
                y=puts_strike_grid,
                colorscale='Viridis'
            )])

        fig.update_layout(
            title="Implied Volatility Surface",
            scene=dict(
                xaxis_title="Time to Expiry (Years)",
                yaxis_title="Strike Price",
                zaxis_title="Implied Volatility"
            )
        )

        st.plotly_chart(fig)
    else:
        st.error("Failed to retrieve data from backend.")