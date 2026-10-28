import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="OrderBlock Liquidity Architecture",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    .block-container { padding: 0 !important; max-width: 100% !important; }
    header, footer { display: none !important; }
    div[data-testid="stVerticalBlock"] { gap: 0 !important; }
</style>
""", unsafe_allow_html=True)

with open("index.html", "r", encoding="utf-8") as f:
    html_content = f.read()

# Responsive iframe height matching viewport
components.html(html_content, height=780, scrolling=True)
