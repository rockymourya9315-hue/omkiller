import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="OrderBlock Pro Engine", layout="wide", initial_sidebar_state="collapsed")

html_code = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=0.85">
<script src="https://d3js.org/d3.v7.min.js"></script>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
  body { background-color: #0d1117; color: #e6edf3; padding: 10px; overflow-x: auto; user-select: none; }
  .top-stats { display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #21262d; padding-bottom: 8px; margin-bottom: 10px; }
  .counter-box { background: #161b22; border: 1px solid #30363d; border-radius: 6px; padding: 4px 12px; font-size: 12px; font-weight: 600; }
  #main-viewport { position: relative; width: 1100px; height: 680px; }
  svg { width: 100%; height: 100%; }
  .flow-curve { fill: none; opacity: 0.28; transition: opacity 0.2s, stroke-width 0.2s; }
  .flow-curve:hover { opacity: 0.95; stroke-width: 2.2px !important; }
  .ladder-tick { stroke-width: 1.5; opacity: 0.5; }
  .ladder-bracket { stroke: #388bfd; stroke-width: 2; fill: none; opacity: 0.8; }
  .sec-box { rx: 4px; ry: 4px; fill: #161b22; stroke: #30363d; }
  .sec-label { font-size: 11px; fill: #c9d1d9; font-weight: 600; pointer-events: none; }
  .sec-pct { font-size: 10px; font-weight: bold; pointer-events: none; }
  .card-box { rx: 5px; ry: 5px; cursor: pointer; transition: 0.15s; }
  .card-box:hover { filter: drop-shadow(0 0 6px rgba(16, 185, 129, 0.4)); }
  .card-title { font-size: 12px; font-weight: 700; fill: #ffffff; pointer-events: none; }
  .card-sub { font-size: 10px; fill: #8b949e; pointer-events: none; }
  .card-tag { font-size: 9px; font-weight: 700; pointer-events: none; }
  .modal-overlay { display: none; position: fixed; inset: 0; background: rgba(0,0,0,0.85); z-index: 999; justify-content: center; align-items: center; }
  .modal-window { background: #161b22; border: 1px solid #30363d; border-radius: 8px; width: 440px; padding: 16px; }
  .close-x { float: right; background: none; border: none; color: #8b949e; font-size: 20px; cursor: pointer; }
  .ob-highlight { background: rgba(16, 185, 129, 0.15); border: 1px dashed #10b981; border-radius: 4px; padding: 10px; margin: 12px 0; font-size: 12px; }
  .grid-metrics { display: grid; grid-template-columns: repeat(3, 1fr); gap: 6px; font-size: 11px; background: #0d1117; padding: 8px; border-radius: 4px; }
</style>
</head>
<body>
<div class="top-stats">
  <div style="font-size: 13px; font-weight: 700; letter-spacing: 0.5px;">ORDERBLOCK LIQUIDITY FLOW</div>
  <div class="counter-box">
    BULLISH <span style="color:#10b981;">172</span> &nbsp;|&nbsp; BEARISH <span style="color:#ef4444;">41</span>
  </div>
</div>
<div id="main-viewport">
  <svg id="chart-svg"></svg>
</div>
<div class="modal-overlay" id="info-modal">
  <div class="modal-window">
    <button class="close-x" onclick="closePopup()">✕</button>
    <div style="font-size:16px; font-weight:bold;" id="popStock">STOCK</div>
    <div style="font-size:11px; color:#8b949e; margin-bottom:8px;" id="popSector">SECTOR</div>
    <div style="font-size:22px; font-weight:bold;" id="popPrice">₹0.00</div>
    <div style="font-size:12px; margin-bottom:10px;" id="popPct">+0.00%</div>
    <div class="ob-highlight">
      <strong>🎯 ORDER BLOCK DETECTED:</strong> <span id="popZone">10:00 AM Open Range</span><br>
      Liquidity Sweep: <span style="color:#10b981; font-weight:bold;">Long Build-Up Confirmed</span>
    </div>
    <div class="grid-metrics">
      <div>VWAP: <b style="color:white;" id="popVwap">0.00</b></div>
      <div>OI SURGE: <b style="color:#10b981;" id="popOi">+13.4%</b></div>
      <div>CONV: <b style="color:white;">98/100</b></div>
      <div>SUPPORT: <b style="color:white;" id="popSup">0.00</b></div>
      <div>RESIST: <b style="color:white;" id="popRes">0.00</b></div>
      <div>BIAS: <b style="color:#10b981;">BULLISH
