import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="Personal Market Scanner", layout="wide")

st.markdown("""
    <style>
    .metric-card {
        background-color: #161b22;
        border: 1px solid #30363d;
        border-radius: 8px;
        padding: 12px;
        margin-bottom: 10px;
    }
    .bullish-text { color: #00e676; font-weight: bold; }
    .bearish-text { color: #ff5252; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

st.title("⚡ Pro Trading Scanner & Sector Breadth")

sectors = {
    "NIFTY BANK": "^NSEBANK",
    "NIFTY IT": "^CNXIT",
    "NIFTY AUTO": "^CNXAUTO",
    "NIFTY METAL": "^CNXMETAL",
    "NIFTY PHARMA": "^CNXPHARMA",
    "NIFTY FMCG": "^CNXFMCG",
    "NIFTY ENERGY": "^CNXENERGY"
}

st.subheader("📊 Sector Momentum")
sec_cols = st.columns(len(sectors))
sec_idx = 0

for sec_name, symbol in sectors.items():
    try:
        t = yf.Ticker(symbol)
        h = t.history(period="2d")
        if len(h) >= 2:
            pct = ((h['Close'].iloc[-1] - h['Close'].iloc[-2]) / h['Close'].iloc[-2]) * 100
            val = round(pct, 2)
            arrow = "▲" if val >= 0 else "▼"
            sec_cols[sec_idx].metric(label=sec_name.replace("NIFTY ", ""), value=f"{val}%", delta=f"{arrow} {val}%")
    except Exception:
        pass
    sec_idx += 1

st.divider()

stocks = [
    "RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "INFY.NS", "ICICIBANK.NS", 
    "TATAMOTORS.NS", "SBIN.NS", "BHARTIARTL.NS", "LT.NS", "AXISBANK.NS",
    "ITC.NS", "MARUTI.NS", "SUNPHARMA.NS", "TITAN.NS", "TATASTEEL.NS"
]

st.subheader("🎯 High Volume & Breakout Setups")

data_list = []
bull_count = 0
bear_count = 0

for s in stocks:
    try:
        ticker = yf.Ticker(s)
        df = ticker.history(period="5d")
        if len(df) >= 2:
            prev_close = df['Close'].iloc[-2]
            curr_close = df['Close'].iloc[-1]
            high_prev = df['High'].iloc[-2]
            low_prev = df['Low'].iloc[-2]
            curr_volume = df['Volume'].iloc[-1]
            avg_volume = df['Volume'].iloc[:-1].mean()
            
            change_pct = ((curr_close - prev_close) / prev_close) * 100
            vol_surge = curr_volume > (avg_volume * 1.3)
            
            setup = "Normal"
            if curr_close > high_prev and vol_surge:
                setup = "🚀 Bullish Breakout"
                bull_count += 1
            elif curr_close < low_prev and vol_surge:
                setup = "🔻 Bearish Breakdown"
                bear_count += 1
            elif change_pct > 0.8:
                setup = "🟢 Strong Momentum"
                bull_count += 1
            elif change_pct < -0.8:
                setup = "🔴 Strong Pullback"
                bear_count += 1
            else:
                setup = "⚪ Rangebound"

            data_list.append({
                "Stock": s.replace(".NS", ""),
                "Price (₹)": round(curr_close, 2),
                "Change %": f"{round(change_pct, 2)}%",
                "Volume Surge": "🔥 Yes" if vol_surge else "No",
                "Action Setup": setup
            })
    except Exception:
        continue

c1, c2 = st.columns(2)
c1.metric("Market Breadth (Bullish)", f"{bull_count} Stocks", delta="Green Flow")
c2.metric("Market Breadth (Bearish)", f"{bear_count} Stocks", delta="-Red Flow", delta_color="inverse")

if data_list:
    final_df = pd.DataFrame(data_list)
    st.dataframe(final_df, use_container_width=True)
else:
    st.info("Market data fetch ho raha hai...")
