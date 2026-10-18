import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="OrderBlock D3 Engine", layout="wide", initial_sidebar_state="collapsed")

d3_sankey_html = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<!-- Load D3.js Official Library -->
<script src="https://d3js.org/d3.v7.min.js"></script>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, sans-serif; }
  body { background-color: #0b0f17; color: #e6edf3; padding: 12px; overflow-x: auto; }
  
  .header { display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #21262d; padding-bottom: 8px; margin-bottom: 12px; }
  .badge { background: #161b22; border: 1px solid #30363d; border-radius: 6px; padding: 4px 10px; font-size: 11px; }
  .bull { color: #10b981; font-weight: bold; }
  .bear { color: #ef4444; font-weight: bold; }

  #viz-container { position: relative; width: 920px; height: 500px; }
  svg { width: 100%; height: 100%; }

  /* D3 Flow Styles */
  .flow-line { fill: none; opacity: 0.45; transition: opacity 0.2s, stroke-width 0.2s; }
  .flow-line:hover { opacity: 0.9; stroke-width: 3.5px !important; }
  .node-box { rx: 4px; ry: 4px; cursor: pointer; }
  .node-text { font-size: 11px; fill: #e6edf3; font-weight: 500; pointer-events: none; }
  .pct-text { font-size: 10px; font-weight: bold; pointer-events: none; }

  /* Modal */
  .modal-overlay { display: none; position: fixed; inset: 0; background: rgba(0,0,0,0.85); z-index: 999; justify-content: center; align-items: center; }
  .modal-card { background: #161b22; border: 1px solid #30363d; border-radius: 8px; width: 90%; max-width: 440px; padding: 16px; }
  .modal-close { float: right; background: none; border: none; color: #8b949e; font-size: 20px; cursor: pointer; }
  .ob-box { background: rgba(16, 185, 129, 0.12); border: 1px dashed #10b981; border-radius: 4px; padding: 10px; margin: 12px 0; font-size: 12px; }
  .modal-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 6px; font-size: 11px; background: #0d1117; padding: 8px; border-radius: 4px; }
</style>
</head>
<body>

<div class="header">
  <div style="font-size:14px; font-weight:bold;">ORDERBLOCK FLOW D3 ENGINE</div>
  <div class="badge">▲ <span class="bull">172</span> | ▼ <span class="bear">41</span></div>
</div>

<div id="viz-container">
  <svg id="canvas"></svg>
</div>

<!-- Interactive Modal -->
<div class="modal-overlay" id="modal">
  <div class="modal-card">
    <button class="modal-close" onclick="closeModal()">✕</button>
    <div style="font-size:16px; font-weight:bold;" id="mStock">STOCK</div>
    <div style="font-size:11px; color:#8b949e; margin-bottom:8px;" id="mSector">SECTOR</div>
    <div style="font-size:22px; font-weight:bold;" id="mPrice">₹0.00</div>
    <div style="font-size:12px; margin-bottom:10px;" id="mPct">+0.00%</div>
    
    <div class="ob-box">
      <strong>🎯 ORDER BLOCK ZONE:</strong> <span id="mZone">10:00 AM Session</span><br>
      Accumulation Level: <span style="color:#10b981; font-weight:bold;">Breakout Zone</span>
    </div>

    <div class="modal-grid">
      <div>VWAP: <b style="color:white;" id="mVwap">7,015.20</b></div>
      <div>OI: <b style="color:#10b981;">+14.2%</b></div>
      <div>CONF: <b style="color:white;">98/100</b></div>
    </div>
  </div>
</div>

<script>
// 1. Data Definitions
const sectors = [
  { id: 'sec_auto', name: 'AUTO', pct: '+2.87%', type: 'bull', y: 30 },
  { id: 'sec_cement', name: 'CEMENT', pct: '+2.22%', type: 'bull', y: 80 },
  { id: 'sec_fin', name: 'FINANCE', pct: '+1.04%', type: 'bull', y: 130 },
  { id: 'sec_it', name: 'IT', pct: '+0.81%', type: 'bull', y: 180 },
  { id: 'sec_metal', name: 'METAL', pct: '+0.52%', type: 'bull', y: 230 },
  { id: 'sec_realty', name: 'REALTY', pct: '-0.34%', type: 'bear', y: 290 },
  { id: 'sec_fmcg', name: 'FMCG', pct: '-0.88%', type: 'bear', y: 340 },
  { id: 'sec_media', name: 'MEDIA', pct: '-1.12%', type: 'bear', y: 390 },
  { id: 'sec_oil', name: 'OIL & GAS', pct: '-1.45%', type: 'bear', y: 440 }
];

const stocks = [
  { id: 'st_eicher', name: 'EICHERMOT', sec: 'AUTO', pct: '+4.17%', price: '7,058.00', type: 'bull', y: 40, vwap: '7,015.20' },
  { id: 'st_tvs', name: 'TVSMOTOR', sec: 'AUTO', pct: '+1.71%', price: '2,480.00', type: 'bull', y: 105, vwap: '2,455.00' },
  { id: 'st_inox', name: 'INOXWIND', sec: 'ENERGY', pct: '+6.76%', price: '142.10', type: 'bull', y: 170, vwap: '136.50' },
  { id: 'st_tcs', name: 'TCS', sec: 'IT', pct: '+3.92%', price: '4,120.00', type: 'bull', y: 235, vwap: '4,070.00' },
  { id: 'st_anand', name: 'ANANDRATHI', sec: 'FINANCE', pct: '-4.68%', price: '2,038.20', type: 'bear', y: 320, vwap: '2,090.00' },
  { id: 'st_mphasis', name: 'MPHASIS', sec: 'IT', pct: '-2.14%', price: '2,610.00', type: 'bear', y: 385, vwap: '2,650.00' },
  { id: 'st_itc', name: 'ITC', sec: 'FMCG', pct: '-1.25%', price: '488.00', type: 'bear', y: 450, vwap: '494.00' }
];

const links = [
  { sourceY: 30, targetY: 40, type: 'bull' },
  { sourceY: 30, targetY: 105, type: 'bull' },
  { sourceY: 80, targetY: 40, type: 'bull' },
  { sourceY: 180, targetY: 235, type: 'bull' },
  { sourceY: 130, targetY: 170, type: 'bull' },
  { sourceY: 290, targetY: 320, type: 'bear' },
  { sourceY: 340, targetY: 450, type: 'bear' },
  { sourceY: 180, targetY: 385, type: 'bear' },
  { sourceY: 440, targetY: 320, type: 'bear' }
];

// 2. D3 Rendering
const svg = d3.select("#canvas");

// Draw Flow Lines using D3 Link Generator (Bézier curves)
const linkGen = d3.linkHorizontal()
  .source(d => [140, d.sourceY + 15])
  .target(d => [620, d.targetY + 20]);

svg.selectAll(".flow-line")
  .data(links)
  .enter()
  .append("path")
  .attr("class", "flow-line")
  .attr("d", linkGen)
  .attr("stroke", d => d.type === 'bull' ? '#10b981' : '#ef4444')
  .attr("stroke-width", 1.8);

// Draw Middle Bracket Flow
svg.append("line")
  .attr("x1", 380).attr("y1", 20)
  .attr("x2", 380).attr("y2", 480)
  .attr("stroke", "#30363d")
  .attr("stroke-dasharray", "4,4")
  .attr("stroke-width", 2);

// Draw Sector Nodes (Left)
const secGroups = svg.selectAll(".sec-node")
  .data(sectors)
  .enter()
  .append("g")
  .attr("transform", d => `translate(10, ${d.y})`);

secGroups.append("rect")
  .attr("width", 130).attr("height", 30)
  .attr("class", "node-box")
  .attr("fill", "#161b22")
  .attr("stroke", "#30363d");

secGroups.append("text")
  .attr("x", 10).attr("y", 19)
  .attr("class", "node-text")
  .text(d => d.name);

secGroups.append("text")
  .attr("x", 120).attr("y", 19)
  .attr("text-anchor", "end")
  .attr("class", "pct-text")
  .attr("fill", d => d.type === 'bull' ? '#10b981' : '#ef4444')
  .text(d => d.pct);

// Draw Stock Cards (Right)
const stockGroups = svg.selectAll(".stock-node")
  .data(stocks)
  .enter()
  .append("g")
  .attr("transform", d => `translate(620, ${d.y})`)
  .style("cursor", "pointer")
  .on("click", (e, d) => openModal(d));

stockGroups.append("rect")
  .attr("width", 260).attr("height", 45)
  .attr("class", "node-box")
  .attr("fill", "#131920")
  .attr("stroke", d => d.type === 'bull' ? '#10b981' : '#ef4444')
  .attr("stroke-width", 1.5);

stockGroups.append("text")
  .attr("x", 12).attr("y", 20)
  .attr("class", "node-text")
  .style("font-weight", "bold")
  .text(d => d.name);

stockGroups.append("text")
  .attr("x", 12).attr("y", 36)
  .attr("fill", "#8b949e")
  .style("font-size", "10px")
  .text(d => "₹" + d.price);

stockGroups.append("text")
  .attr("x", 248).attr("y", 22)
  .attr("text-anchor", "end")
  .attr("class", "pct-text")
  .attr("fill", d => d.type === 'bull' ? '#10b981' : '#ef4444')
  .text(d => d.pct);

stockGroups.append("text")
  .attr("x", 248).attr("y", 36)
  .attr("text-anchor", "end")
  .attr("fill", d => d.type === 'bull' ? '#10b981' : '#ef4444')
  .style("font-size", "9px")
  .text(d => d.type === 'bull' ? 'BUY BLOCK' : 'SELL BLOCK');

// Modal Logic
function openModal(d) {
  document.getElementById('mStock').innerText = d.name;
  document.getElementById('mSector').innerText = d.sec + ' SECTOR';
  document.getElementById('mPrice').innerText = '₹' + d.price;
  const p = document.getElementById('mPct');
  p.innerText = d.pct;
  p.className = d.type === 'bull' ? 'bull' : 'bear';
  document.getElementById('mVwap').innerText = d.vwap;
  document.getElementById('modal').style.display = 'flex';
}

function closeModal() {
  document.getElementById('modal').style.display = 'none';
}
</script>
</body>
</html>
"""

components.html(d3_sankey_html, height=580, scrolling=True)
