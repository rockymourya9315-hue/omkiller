import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="Market Scanner", layout="wide")

st.title("📊 Live Market Scanner")

# Watchlist stocks
stocks = ["RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "INFY.NS", "ICICIBANK.NS", "TATAMOTORS.NS"]

data_list = []

for symbol in stocks:
    try:
        ticker = yf.Ticker(symbol)
        df = ticker.history(period="2d")
        if len(df) >= 2:
            prev_close = df['Close'].iloc[-2]
            curr_price = df['Close'].iloc[-1]
            change_pct = ((curr_price - prev_close) / prev_close) * 100
            volume = df['Volume'].iloc[-1]
            
            status = "🟢 Bullish" if change_pct > 0.5 else ("🔴 Bearish" if change_pct < -0.5 else "⚪ Neutral")
            
            data_list.append({
                "Stock": symbol.replace(".NS", ""),
                "Price (₹)": round(curr_price, 2),
                "Change %": f"{round(change_pct, 2)}%",
                "Signal": status,
                "Volume": volume
            })
    except Exception:
        continue

if data_list:
    result_df = pd.DataFrame(data_list)
    st.dataframe(result_df, use_container_width=True)
else:
    st.write("Data load ho raha hai, thoda wait karein...")
  
