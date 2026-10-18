import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="OrderBlock", layout="wide", initial_sidebar_state="collapsed")

with open("index.html", "r", encoding="utf-8") as f:
    html_data = f.read()

components.html(html_data, height=720, scrolling=True)
