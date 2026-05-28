import streamlit as st
import yfinance as yf
from datetime import datetime
import pandas as pd
from datetime import timedelta

st.title('Equity Return Analysis')

# Sample data - can be replaced with user input
initial_data = [
    {'Company': 'Visa Inc.', 'Ticker': 'V', 'Exchange': 'NYSE', 'Purchase Date': '2026-05-21'},
    {'Company': 'Danaos Corporation', 'Ticker': 'DAC', 'Exchange': 'NYSE', 'Purchase Date': '2026-05-21'},
    {'Company': 'Morgan Stanley', 'Ticker': 'MS', 'Exchange': 'NYSE', 'Purchase Date': '2026-05-21'},
    {'Company': 'Arm Holdings plc', 'Ticker': 'ARM', 'Exchange': 'NASDAQ', 'Purchase Date': '2026-05-21'},
    {'Company': 'Taiwan Semiconductor Manufacturing Co.', 'Ticker': 'TSM', 'Exchange': 'NYSE', 'Purchase Date': '2026-05-21'},
    {'Company': 'Bloom Energy Corporation', 'Ticker': 'BE', 'Exchange': 'NYSE', 'Purchase Date': '2026-05-21'},
    {'Company': 'Boeing Company', 'Ticker': 'BA', 'Exchange': 'NYSE', 'Purchase Date': '2026-05-21'},
    {'Company': 'NVIDIA Corporation', 'Ticker': 'NVDA', 'Exchange': 'NASDAQ', 'Purchase Date': '2026-05-21'},
    {'Company': 'Philip Morris International', 'Ticker': 'PM', 'Exchange': 'NYSE', 'Purchase Date': '2026-05-21'},
    {'Company': 'Invesco Water Resources ETF', 'Ticker': 'PHO', 'Exchange': 'NASDAQ', 'Purchase Date': '2026-05-21'}
]

# Fetch historical price on purchase date
results = []
for data in initial_data:
    company = data['Company']
    ticker = data['Ticker']
    exchange = data['Exchange']
    purchase_date_str = data['Purchase Date']
    
    # Convert to datetime object
    purchase_date = datetime.strptime(purchase_date_str, '%Y-%m-%d')
    
    # Fetch historical price
    stock = yf.Ticker(ticker)
    hist = stock.history(
    start=purchase_date.strftime('%Y-%m-%d'),
    end=(purchase_date + timedelta(days=1)).strftime('%Y-%m-%d')
)
    purchase_price = hist['Close'].iloc[0] if not hist.empty else None
    
    # Calculate returns
    current_price = stock.info.get('currentPrice')
    change_percent = ((current_price - purchase_price)/purchase_price)*100 if purchase_price else 0
    
    results.append({
        'Company': company,
        'Ticker': ticker,
        'Exchange': exchange,
        'Purchase Date': purchase_date_str,
        'Purchase Price': f'${purchase_price:.2f}' if purchase_price else 'N/A',
        'Current Price': f'${current_price:.2f}' if current_price else 'N/A',
        'Percentage Change': f'{change_percent:.1f}%' if purchase_price else 'N/A'
    })

# Display results
st.write('This app shows the return on equities bought on specific dates.')
st.dataframe(pd.DataFrame(results))
