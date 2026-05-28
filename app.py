import streamlit as st
import pandas as pd
import yfinance as yf

st.title('Portfolio Tracker')

portfolio = [
    {
        'Name': 'Apple Inc.',
        'Ticker': 'AAPL',
        'Stock Exchange': 'New York',
        'Date of Purchase': '2024-02-15',
        'Price at Purchase': 190.25,
    },
    {
        'Name': 'Microsoft Corp.',
        'Ticker': 'MSFT',
        'Stock Exchange': 'New York',
        'Date of Purchase': '2025-01-10',
        'Price at Purchase': 340.75,
    },
    {
        'Name': 'Shell UK Plc',
        'Ticker': 'SHEL.L',
        'Stock Exchange': 'London',
        'Date of Purchase': '2024-08-05',
        'Price at Purchase': 120.50,
    },
]

rows = []
for position in portfolio:
    ticker = position['Ticker']
    try:
        stock = yf.Ticker(ticker)
        current_price = None
        if hasattr(stock, 'fast_info') and stock.fast_info is not None:
            current_price = stock.fast_info.last_price
        if current_price is None:
            hist = stock.history(period='5d')
            if not hist.empty:
                current_price = hist['Close'].iloc[-1]

        if current_price is None:
            current_price = 0.0

        percent_change = 0.0
        if position['Price at Purchase']:
            percent_change = ((current_price - position['Price at Purchase']) / position['Price at Purchase']) * 100

        rows.append({
            'Name': position['Name'],
            'Ticker': ticker,
            'Stock Exchange': position['Stock Exchange'],
            'Date of Purchase': position['Date of Purchase'],
            'Price at Purchase': position['Price at Purchase'],
            'Price Now': round(current_price, 2),
            '% Change': f"{percent_change:.2f}%",
        })
    except Exception as exc:
        rows.append({
            'Name': position['Name'],
            'Ticker': ticker,
            'Stock Exchange': position['Stock Exchange'],
            'Date of Purchase': position['Date of Purchase'],
            'Price at Purchase': position['Price at Purchase'],
            'Price Now': 'N/A',
            '% Change': 'N/A',
        })

st.table(pd.DataFrame(rows))


