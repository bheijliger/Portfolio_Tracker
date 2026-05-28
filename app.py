```python
import streamlit as st
import yfinance as yf
import pandas as pd

from datetime import datetime, timedelta

st.set_page_config(page_title="Equity Return Analysis", layout="wide")

st.title("Equity Return Analysis")

st.write(
    "This app calculates the return on equities purchased on a given date."
)

# IMPORTANT:
# Purchase dates must be REAL past dates
# not future dates

initial_data = [
    {"Company": "Visa Inc.", "Ticker": "V", "Exchange": "NYSE", "Purchase Date": "2025-05-21"},
    {"Company": "Danaos Corporation", "Ticker": "DAC", "Exchange": "NYSE", "Purchase Date": "2025-05-21"},
    {"Company": "Morgan Stanley", "Ticker": "MS", "Exchange": "NYSE", "Purchase Date": "2025-05-21"},
    {"Company": "Arm Holdings plc", "Ticker": "ARM", "Exchange": "NASDAQ", "Purchase Date": "2025-05-21"},
    {"Company": "Taiwan Semiconductor Manufacturing Co.", "Ticker": "TSM", "Exchange": "NYSE", "Purchase Date": "2025-05-21"},
    {"Company": "Bloom Energy Corporation", "Ticker": "BE", "Exchange": "NYSE", "Purchase Date": "2025-05-21"},
    {"Company": "Boeing Company", "Ticker": "BA", "Exchange": "NYSE", "Purchase Date": "2025-05-21"},
    {"Company": "NVIDIA Corporation", "Ticker": "NVDA", "Exchange": "NASDAQ", "Purchase Date": "2025-05-21"},
    {"Company": "Philip Morris International", "Ticker": "PM", "Exchange": "NYSE", "Purchase Date": "2025-05-21"},
    {"Company": "Invesco Water Resources ETF", "Ticker": "PHO", "Exchange": "NASDAQ", "Purchase Date": "2025-05-21"},
]

results = []

with st.spinner("Fetching market data..."):

    for data in initial_data:

        company = data["Company"]
        ticker = data["Ticker"]
        exchange = data["Exchange"]
        purchase_date_str = data["Purchase Date"]

        try:

            stock = yf.Ticker(ticker)

            # Convert purchase date
            purchase_date = datetime.strptime(
                purchase_date_str,
                "%Y-%m-%d"
            )

            # Yahoo Finance end date is EXCLUSIVE
            next_day = purchase_date + timedelta(days=1)

            # Historical purchase price
            hist = stock.history(
                start=purchase_date.strftime("%Y-%m-%d"),
                end=next_day.strftime("%Y-%m-%d")
            )

            if not hist.empty:
                purchase_price = float(hist["Close"].iloc[0])
            else:
                purchase_price = None

            # Current price
            current_hist = stock.history(period="1d")

            if not current_hist.empty:
                current_price = float(current_hist["Close"].iloc[-1])
            else:
                current_price = None

            # Percentage return
            if purchase_price is not None and current_price is not None:

                change_percent = (
                    (current_price - purchase_price)
                    / purchase_price
                ) * 100

            else:
                change_percent = None

            results.append({
                "Company": company,
                "Ticker": ticker,
                "Exchange": exchange,
                "Purchase Date": purchase_date_str,
                "Purchase Price": (
                    f"${purchase_price:,.2f}"
                    if purchase_price is not None
                    else "N/A"
                ),
                "Current Price": (
                    f"${current_price:,.2f}"
                    if current_price is not None
                    else "N/A"
                ),
                "Percentage Change": (
                    f"{change_percent:.2f}%"
                    if change_percent is not None
                    else "N/A"
                )
            })

        except Exception as e:

            results.append({
                "Company": company,
                "Ticker": ticker,
                "Exchange": exchange,
                "Purchase Date": purchase_date_str,
                "Purchase Price": "Error",
                "Current Price": "Error",
                "Percentage Change": str(e)
            })

# Create dataframe
df = pd.DataFrame(results)

# Display dataframe
st.dataframe(
    df,
    use_container_width=True,
    hide_index=True
)

# Optional download button
csv = df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download Results as CSV",
    data=csv,
    file_name="equity_returns.csv",
    mime="text/csv"
)

