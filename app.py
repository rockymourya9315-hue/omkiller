import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Order Block", layout="wide", initial_sidebar_state="collapsed")

# Margin aur padding hatane ke liye custom CSS
st.markdown("""
<style>
    .block-container { padding: 0 !important; max-width: 100% !important; }
    header, footer { display: none !important; }
</style>
""", unsafe_allow_html=True)

with open("index.html", "r", encoding="utf-8") as f:
    html_content = f.read()

components.html(html_content, height=820, scrolling=False)
