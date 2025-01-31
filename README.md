# Volatility Surface Explorer

A web application to compute and visualize the **implied volatility (IV) surface** for options using the **Black-Scholes model**. The backend fetches option chain data and computes IVs, while the frontend displays the IV surface using **Streamlit** and **Plotly**.

---

## Features
- Fetch option chain data (calls and puts) from financial APIs using `yfinance`.
- Calculate implied volatilities for options using the Black-Scholes model.
- Display a 3D surface of implied volatilities for selected tickers, strikes, and expiries.
- Identify option premium inefficiencies by analyzing the IV surface.

## Project Structure
```
vol_surface_explorer
├── backend
│   ├── src
│   │   ├── run.py              # Flask app to serve the backend API
│   │   ├── fetch_data.py       # Fetch option chain data using yfinance
│   │   ├── black_scholes.py    # Calculate implied volatility using the Black-Scholes model
│   │   └── __init__.py         # Optional: Can leave empty
├── frontend
│   └── app.py                  # Streamlit app for the UI to display the IV surface
├── .env                        # Store API keys and secrets (not included in version control)
├── README.md                   # This file
├── requirements.txt            # Required Python packages
├── .gitignore                  # Ignoring sensitive files like .env and unnecessary caches
└── calls.csv                   # Optional: Example option data for testing
```

---
## Installation - MacOS Users

### Local Environment Setup <a name="Local_Environment_Setup"></a>

First, download the repository.

### Clone the repository

```
git clone https://github.com/alshodiev/vol_surface_explorer.git
cd vol_surface_explorer
```
Now, create the environment.

```
python -m venv vol_explorer
source vol_explorer/bin/activate    # For MacOS/Linux
```

### Install Dependencies and Set up Environment Variables
```
# .env file
POLYGON_API_KEY=your_polygon_api_key_here
```
## Running the Application
### Start the Backend
```
cd backend/src
python run.py
```

The backend should run on http://127.0.0.1:5000 but the port number can still be changed if other servers are running on port=5000

### Start the Frontend
```
cd frontend
streamlit run app.py
```

## Future Steps
- Add support for advanced option pricing models (e.g., Heston, SABR).
- Enable real-time data fetching and updates.
- Introduce user-defined IV caps and filters for better surface control.








