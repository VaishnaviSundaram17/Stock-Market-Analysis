import streamlit as st
import yfinance as yf
import pandas as pd
import altair as alt

# 🎯 Set Streamlit Page Configuration
st.set_page_config(page_title="Stock Data Analyzer", layout="wide")

# 🏷️ Title
st.title("📈 Stock Data Analyzer")

# 🔹 Step 1: Enter the Stock Symbol
st.sidebar.header("Stock Selection")
stock_symbol = st.sidebar.text_input("Enter Stock Symbol (e.g., AAPL, TSLA, MSFT)", "AAPL")

# 🔹 Step 2: Select Date Range
st.sidebar.header("Select Date Range")
start_date = st.sidebar.date_input("Start Date", pd.to_datetime("2024-01-01"))
end_date = st.sidebar.date_input("End Date", pd.to_datetime("today"))

# 🚀 Fetch Data Button
if st.sidebar.button("Get Stock Data"):
    with st.spinner("Fetching data..."):
        try:
            # Fetch Stock Data
            stock_data = yf.download(stock_symbol, start=start_date, end=end_date)

            # Check if data is available
            if stock_data.empty:
                st.error("⚠️ No data found! Please check the stock symbol or date range.")
            else:
                # ✅ Flatten MultiIndex Columns (Fix for KeyError)
                if isinstance(stock_data.columns, pd.MultiIndex):
                    stock_data.columns = stock_data.columns.get_level_values(0)

                # Reset index to show Date as a column
                stock_data.reset_index(inplace=True)

                # 📊 Display the Data
                st.subheader(f"📊 {stock_symbol} Stock Data ({start_date} to {end_date})")
                st.write(stock_data)

                # 📈 Show OHLCV Chart
                st.subheader("📉 Price Trend")
                st.line_chart(stock_data.set_index("Date")[['Open', 'High', 'Low', 'Close']])

                # 📊 Show Volume Chart (Ensuring data availability)
                if 'Volume' in stock_data.columns:
                    st.subheader("📊 Volume Trend")
                    volume_chart = alt.Chart(stock_data).mark_bar().encode(
                        x=alt.X('Date:T', title="Date"),  # Date on x-axis
                        y=alt.Y('Volume:Q', title="Trading Volume"),
                        tooltip=['Date', 'Volume']
                    ).properties(
                        title="📊 Volume Trend"
                    )
                    st.altair_chart(volume_chart, use_container_width=True)
                else:
                    st.warning("⚠️ Volume data not available for the selected stock.")
        except Exception as e:
            st.error(f"⚠️ Error fetching data: {e}")
