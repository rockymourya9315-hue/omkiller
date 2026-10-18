import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="OrderBlock Pro Engine", layout="wide", initial_sidebar_state="collapsed")

dense_flow_html = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=0.85">
<script src="https://d3js.org/d3.v7.min.js"></script>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
  body { background-color: #0d1117; color: #e6edf3; padding: 10px; overflow-x: auto; user-select: none; }

  /* Top Bar */
  .top-stats { display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #21262d; padding-bottom: 8px; margin-bottom: 10px; }
  .counter-box { background: #161b22; border: 1px solid #30363d; border-radius: 6px; padding: 4px 12px; font-size: 12px; font-weight: 600; }

  /* Main Canvas Container */
  #main-viewport { position: relative; width: 1100px; height: 680px; }
  svg { width: 100%; height: 100%; }

  /* Dense SVG Web Flow */
  .flow-curve { fill: none; opacity: 0.28; transition: opacity 0.2s, stroke-width 0.2s; }
  .flow-curve:hover { opacity: 0.95; stroke-width: 2.2px !important; }
  
  /* Middle Dense Ladder */
  .ladder-tick { stroke-width: 1.5; opacity: 0.5; }
  .ladder-bracket { stroke: #388bfd; stroke-width: 2; fill: none; opacity: 0.8; }

  /* Nodes & Text */
  .sec-box { rx: 4px; ry: 4px; fill: #161b22; stroke: #30363d; }
  .sec-label { font-size: 11px; fill: #c9d1d9; font-weight: 600; pointer-events: none; }
  .sec-pct { font-size: 10px; font-weight: bold; pointer-events: none; }

  /* Stock Cards */
  .card-box { rx: 5px; ry: 5px; cursor: pointer; transition: 0.15s; }
  .card-box:hover { filter: drop-shadow(0 0 6px rgba(16, 185, 129, 0.4)); }
  .card-title { font-size: 12px; font-weight: 700; fill: #ffffff; pointer-events: none; }
  .card-sub { font-size: 10px; fill: #8b949e; pointer-events: none; }
  .card-tag { font-size: 9px; font-weight: 700; pointer-events: none; }

  /* Modal Popup */
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

<!-- Modal Details -->
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
      <div>BIAS: <b style="color:#10b981;">BULLISH</b></div>
    </div>
  </div>
</div>

<script>
// Data Setup
const sectors = [
  { id: 0, name: "AUTO", pct: "+2.87%", type: "bull", y: 20 },
  { id: 1, name: "LOGISTICS", pct: "+2.41%", type: "bull", y: 62 },
  { id: 2, name: "CEMENT", pct: "+2.22%", type: "bull", y: 104 },
  { id: 3, name: "FINANCE", pct: "+1.95%", type: "bull", y: 146 },
  { id: 4, name: "NBFC", pct: "+1.38%", type: "bull", y: 188 },
  { id: 5, name: "IT", pct: "+1.14%", type: "bull", y: 230 },
  { id: 6, name: "INFRA", pct: "+0.85%", type: "bull", y: 272 },
  { id: 7, name: "PHARMA", pct: "+0.45%", type: "bull", y: 314 },
  { id: 8, name: "CHEMICAL", pct: "+0.12%", type: "bull", y: 356 },
  { id: 9, name: "REALTY", pct: "-0.34%", type: "bear", y: 410 },
  { id: 10, name: "FMCG", pct: "-0.78%", type: "bear", y: 452 },
  { id: 11, name: "MEDIA", pct: "-1.10%", type: "bear", y: 494 },
  { id: 12, name: "OIL & GAS", pct: "-1.45%", type: "bear", y: 536 },
  { id: 13, name: "CONSUMER", pct: "-1.82%", type: "bear", y: 578 },
  { id: 14, name: "ENERGY", pct: "-2.30%", type: "bear", y: 620 }
];

const cards = [
  // Top Bullish (Green)
  { id: 0, name: "EICHERMOT", sec: "AUTO", pct: "+4.17%", price: "7,058.00", vwap: "7,015.20", sup: "7,001.00", res: "7,088.00", type: "bull", y: 20 },
  { id: 1, name: "TVSMOTOR", sec: "AUTO", pct: "+2.48%", price: "2,480.00", vwap: "2,460.00", sup: "2,450.00", res: "2,510.00", type: "bull", y: 78 },
  { id: 2, name: "INOXWIND", sec: "ENERGY", pct: "+6.76%", price: "142.10", vwap: "136.50", sup: "138.00", res: "146.00", type: "bull", y: 136 },
  { id: 3, name: "TCS", sec: "IT", pct: "+3.92%", price: "4,120.00", vwap: "4,070.00", sup: "4,050.00", res: "4,160.00", type: "bull", y: 194 },
  { id: 4, name: "AUROPHARMA", sec: "PHARMA", pct: "+2.85%", price: "1,245.00", vwap: "1,228.00", sup: "1,220.00", res: "1,260.00", type: "bull", y: 252 },
  { id: 5, name: "FEDERALBNK", sec: "FINANCE", pct: "+2.11%", price: "192.50", vwap: "189.20", sup: "188.00", res: "195.00", type: "bull", y: 310 },
  // Bearish (Red)
  { id: 6, name: "ANANDRATHI", sec: "FINANCE", pct: "-4.68%", price: "2,038.20", vwap: "2,090.00", sup: "2,010.00", res: "2,080.00", type: "bear", y: 420 },
  { id: 7, name: "MPHASIS", sec: "IT", pct: "-2.14%", price: "2,610.00", vwap: "2,650.00", sup: "2,580.00", res: "2,640.00", type: "bear", y: 478 },
  { id: 8, name: "COFORGE", sec: "IT", pct: "-1.85%", price: "7,450.00", vwap: "7,520.00", sup: "7,380.00", res: "7,510.00", type: "bear", y: 536 },
  { id: 9, name: "ITC", sec: "FMCG", pct: "-1.25%", price: "488.00", vwap: "494.00", sup: "484.00", res: "492.00", type: "bear", y: 594 }
];

const svg = d3.select("#chart-svg");

// 1. Draw Sectors (Left)
const secGroup = svg.selectAll(".sec-g")
  .data(sectors)
