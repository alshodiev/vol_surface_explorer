import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go

st.title("Volatility Surface Explorer")

# User inputs
ticker = st.text_input("Enter the Ticker Symbol", value="AAPL")
min_strike = st.slider("Minimum Strike Price % of Spot", 50, 100, 80)
max_strike = st.slider("Maximum Strike Price % of Spot", 100, 150, 120)
expiry_range = st.slider("Expiry Range (in years)", 0.5, 2.0, (0.5, 1.5))

if st.button("Calculate IV Surface"):
    # Call backend API (assuming it's running locally on port 5000)
    backend_url = f"http://127.0.0.1:5000/calculate_iv_surface"
    response = requests.post(backend_url, json={
        "ticker": ticker,
        "min_strike_pct": min_strike / 100,
        "max_strike_pct": max_strike / 100,
        "expiry_range": expiry_range
    })

    if response.status_code == 200:
        data = response.json()
        df = pd.DataFrame(data)

        # Show raw data
        #st.write("Calculated IV Surface Data:")
        #st.dataframe(df)

        # Plot IV surface
        fig = go.Figure(data=[go.Surface(
            z=df['iv'],
            x=df['expiry'],
            y=df['strike'],
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