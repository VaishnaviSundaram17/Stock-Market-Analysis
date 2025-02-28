import streamlit as st
import yfinance as yf
import pandas as pd
import altair as alt
import ta  # Technical Analysis Library

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

# 🔹 Step 3: Select Data Type to Display
st.sidebar.header("Select Data Type")
option = st.sidebar.radio("Choose an option:", ["Get Data", "Technical Indicators", "Fundamentals"])

# 🚀 Fetch Data
if st.sidebar.button("Fetch Data"):
    with st.spinner("Fetching data..."):
        try:
            # Fetch Stock Data
            stock_data = yf.download(stock_symbol, start=start_date, end=end_date)
            stock_info = yf.Ticker(stock_symbol)
            
            if stock_data.empty:
                st.error("⚠️ No data found! Please check the stock symbol or date range.")
            else:
                stock_data.reset_index(inplace=True)
                stock_data.columns = stock_data.columns.get_level_values(0)  # Flatten MultiIndex Columns

                if option == "Get Data":
                    st.subheader(f"📊 {stock_symbol} Stock Data ({start_date} to {end_date})")
                    st.write(stock_data[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']])
                    
                    # 📈 Price Trend
                    st.subheader("📉 Price Trend")
                    st.line_chart(stock_data.set_index("Date")[['Open', 'High', 'Low', 'Close']])
                    
                    # 📊 Volume Trend
                    if 'Volume' in stock_data.columns:
                        st.subheader("📊 Volume Trend")
                        volume_chart = alt.Chart(stock_data).mark_bar().encode(
                            x=alt.X('Date:T', title="Date"),
                            y=alt.Y('Volume:Q', title="Trading Volume"),
                            tooltip=['Date', 'Volume']
                        ).properties(title="📊 Volume Trend")
                        st.altair_chart(volume_chart, use_container_width=True)
                    
                elif option == "Technical Indicators":
                    st.subheader("📈 Technical Indicators")
                    stock_data['SMA_50'] = ta.trend.sma_indicator(stock_data['Close'], window=50)
                    stock_data['SMA_200'] = ta.trend.sma_indicator(stock_data['Close'], window=200)
                    stock_data['RSI'] = ta.momentum.rsi(stock_data['Close'], window=14)
                    
                    # Display Moving Averages
                    st.line_chart(stock_data.set_index("Date")[['Close', 'SMA_50', 'SMA_200']])
                    
                    # Display RSI
                    st.subheader("📊 RSI Indicator")
                    st.line_chart(stock_data.set_index("Date")['RSI'])
                    
                elif option == "Fundamentals":
                    st.subheader("📊 Fundamentals")
                    try:
                        fundamentals = {
                            "Market Cap": stock_info.info.get("marketCap", "N/A"),
                            "P/E Ratio": stock_info.info.get("trailingPE", "N/A"),
                            "EPS": stock_info.info.get("trailingEps", "N/A"),
                            "Dividend Yield": stock_info.info.get("dividendYield", "N/A"),
                        }
                        st.write(pd.DataFrame(fundamentals.items(), columns=["Metric", "Value"]))
                    except Exception as e:
                        st.error(f"⚠️ Error fetching fundamentals: {e}")
        except Exception as e:
            st.error(f"⚠️ Error fetching data: {e}")

