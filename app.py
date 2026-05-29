import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px

from datetime import datetime

st.set_page_config(
    page_title="Equity Return Analysis",
    layout="wide"
)

st.title("Equity Return Analysis")

st.write(
    """
    This app calculates:

    - Purchase price
    - Current price
    - Total return
    - Daily percentage changes
    - Portfolio-level cumulative returns
    """
)

# =========================================================
# INITIAL DATA
# =========================================================

initial_data = [
    {"Company": "BAE Systems", "Ticker": "BA", "Exchange": "LSE", "Purchase Date": "2026-05-28"},
    {"Company": "Danaos Corporation", "Ticker": "DAC", "Exchange": "NYSE", "Purchase Date": "2026-05-21"},
    {"Company": "Morgan Stanley", "Ticker": "MS", "Exchange": "NYSE", "Purchase Date": "2026-05-21"},
    {"Company": "Arm Holdings plc", "Ticker": "ARM", "Exchange": "NASDAQ", "Purchase Date": "2026-05-21"},
    {"Company": "Taiwan Semiconductor Manufacturing Co.", "Ticker": "TSM", "Exchange": "NYSE", "Purchase Date": "2026-05-21"},
    {"Company": "Bloom Energy Corporation", "Ticker": "BE", "Exchange": "NYSE", "Purchase Date": "2026-05-21"},
    {"Company": "Boeing Company", "Ticker": "BA", "Exchange": "NYSE", "Purchase Date": "2026-05-21"},
    {"Company": "NVIDIA Corporation", "Ticker": "NVDA", "Exchange": "NASDAQ", "Purchase Date": "2026-05-21"},
    {"Company": "Philip Morris International", "Ticker": "PM", "Exchange": "NYSE", "Purchase Date": "2026-05-21"},
    {"Company": "Invesco Water Resources ETF", "Ticker": "PHO", "Exchange": "NASDAQ", "Purchase Date": "2026-05-21"},
]

# =========================================================
# CACHE FUNCTION
# =========================================================

@st.cache_data
def get_stock_history(ticker, start_date):

    stock = yf.Ticker(ticker)

    hist = stock.history(
        start=start_date,
        end=datetime.today().strftime("%Y-%m-%d")
    )

    return hist


# =========================================================
# PROCESS DATA
# =========================================================

results = []
historical_data = {}

with st.spinner("Fetching market data..."):

    for data in initial_data:

        company = data["Company"]
        ticker = data["Ticker"]
        exchange = data["Exchange"]
        purchase_date_str = data["Purchase Date"]

        try:

            purchase_date = datetime.strptime(
                purchase_date_str,
                "%Y-%m-%d"
            )

            # Validate purchase date
            if purchase_date > datetime.today():

                results.append({
                    "Company": company,
                    "Ticker": ticker,
                    "Exchange": exchange,
                    "Purchase Date": purchase_date_str,
                    "Purchase Price": "Invalid",
                    "Current Price": "Invalid",
                    "Percentage Change": "Future date"
                })

                continue

            # Fetch historical data
            hist = get_stock_history(
                ticker,
                purchase_date_str
            )

            # Check if history exists
            if hist.empty:

                results.append({
                    "Company": company,
                    "Ticker": ticker,
                    "Exchange": exchange,
                    "Purchase Date": purchase_date_str,
                    "Purchase Price": "N/A",
                    "Current Price": "N/A",
                    "Percentage Change": "No data"
                })

                continue

            # Purchase & current prices
            purchase_price = float(hist["Close"].iloc[0])
            current_price = float(hist["Close"].iloc[-1])

            # Total return
            change_percent = (
                (current_price - purchase_price)
                / purchase_price
            ) * 100

            # Daily % changes
            hist["Daily % Change"] = (
                hist["Close"].pct_change()
            ) * 100

            # Cumulative return
            hist["Cumulative Return %"] = (
                (hist["Close"] / purchase_price) - 1
            ) * 100

            # Store for later
            historical_data[ticker] = hist

            # Summary results
            results.append({
                "Company": company,
                "Ticker": ticker,
                "Exchange": exchange,
                "Purchase Date": purchase_date_str,
                "Purchase Price": f"${purchase_price:,.2f}",
                "Current Price": f"${current_price:,.2f}",
                "Percentage Change": f"{change_percent:.2f}%"
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

# =========================================================
# SUMMARY TABLE
# =========================================================

st.subheader("Portfolio Summary")

df = pd.DataFrame(results)

st.dataframe(
    df,
    use_container_width=True,
    hide_index=True
)

# =========================================================
# DOWNLOAD BUTTON
# =========================================================

csv = df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download Results as CSV",
    data=csv,
    file_name="equity_returns.csv",
    mime="text/csv"
)

# =========================================================
# PORTFOLIO-LEVEL RETURNS
# =========================================================

st.subheader("Portfolio-Level Cumulative Returns")

portfolio_returns = pd.DataFrame()

for ticker, hist in historical_data.items():

    temp = hist[["Cumulative Return %"]].copy()

    temp.columns = [ticker]

    portfolio_returns = pd.concat(
        [portfolio_returns, temp],
        axis=1
    )

# Average cumulative return across portfolio
portfolio_returns["Portfolio Average Return %"] = (
    portfolio_returns.mean(axis=1)
)

# Reset index for plotting
plot_df = portfolio_returns.reset_index()

fig = px.line(
    plot_df,
    x="Date",
    y="Portfolio Average Return %",
    title="Portfolio Average Cumulative Return"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# Display raw portfolio data
with st.expander("Portfolio Return Data"):

    st.dataframe(
        portfolio_returns.round(2),
        use_container_width=True
    )

# =========================================================
# INDIVIDUAL STOCK ANALYSIS
# =========================================================

st.subheader("Individual Equity Analysis")

for ticker, hist in historical_data.items():

    with st.expander(f"{ticker} Analysis"):

        display_df = hist[[
            "Close",
            "Daily % Change",
            "Cumulative Return %"
        ]].copy()

        display_df = display_df.round(2)

        st.write(f"### {ticker} Daily Performance")

        st.dataframe(
            display_df,
            use_container_width=True
        )

        # =================================================
        # DAILY RETURN CHART
        # =================================================

        daily_fig = px.line(
            display_df.reset_index(),
            x="Date",
            y="Daily % Change",
            title=f"{ticker} Daily Percentage Changes"
        )

        st.plotly_chart(
            daily_fig,
            use_container_width=True
        )

        # =================================================
        # CUMULATIVE RETURN CHART
        # =================================================

        cumulative_fig = px.line(
            display_df.reset_index(),
            x="Date",
            y="Cumulative Return %",
            title=f"{ticker} Cumulative Return Since Purchase"
        )

        st.plotly_chart(
            cumulative_fig,
            use_container_width=True
        )