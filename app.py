import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="OrderBlock", layout="wide", initial_sidebar_state="collapsed")

# Complete Self-Contained App
code = """
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=0.85">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, sans-serif; }
  body { background: #0b0f17; color: #fff; padding: 10px; overflow-x: auto; }
  .top-stats { display: flex; justify-content: space-between; border-bottom: 1px solid #21262d; padding-bottom: 8px; margin-bottom: 10px; font-size: 12px; font-weight: bold; }
  #main-viewport { position: relative; width: 1100px; height: 720px; }
  canvas { position: absolute; left: 0; top: 0; pointer-events: none; z-index: 1; }
  .nodes-layer { position: absolute; left: 0; top: 0; width: 1100px; height: 720px; z-index: 2; }
  .sec-item { position: absolute; width: 140px; height: 32px; background: #161b22; border-radius: 4px; display: flex; justify-content: space-between; align-items: center; padding: 0 10px; font-size: 11px; font-weight: 600; border: 1px solid #30363d; }
  .stock-card { position: absolute; width: 320px; height: 48px; background: #131920; border-radius: 6px; padding: 6px 12px; cursor: pointer; border: 1.5px solid #10b981; }
  .stock-card.bear { border-color: #ef4444; }
  .card-r1 { display: flex; justify-content: space-between; font-weight: bold; font-size: 12px; }
  .card-r2 { display: flex; justify-content: space-between; font-size: 10px; color: #8b949e; margin-top: 2px; }
  .modal-overlay { display: none; position: fixed; inset: 0; background: rgba(0,0,0,0.85); z-index: 99; justify-content: center; align-items: center; }
  .modal-window { background: #161b22; border: 1px solid #30363d; border-radius: 8px; width: 380px; padding: 16px; }
</style>
</head>
<body>
<div class="top-stats">
  <div>ORDERBLOCK LIQUIDITY FLOW</div>
  <div style="background:#161b22; padding:4px 10px; border-radius:4px; border:1px solid #30363d;">
    BULLISH <span style="color:#10b981;">172</span> | BEARISH <span style="color:#ef4444;">41</span>
  </div>
</div>

<div id="main-viewport">
  <canvas id="flowCanvas" width="1100" height="720"></canvas>
  <div class="nodes-layer" id="nodesContainer"></div>
</div>

<div class="modal-overlay" id="info-modal" onclick="this.style.display='none'">
  <div class="modal-window">
    <div style="font-size:16px; font-weight:bold;" id="popStock">STOCK</div>
    <div style="font-size:11px; color:#8b949e; margin-bottom:8px;" id="popSector">SECTOR</div>
    <div style="font-size:20px; font-weight:bold;" id="popPrice">₹0.00</div>
    <div style="margin:10px 0; padding:8px; background:rgba(16,185,129,0.15); border:1px dashed #10b981; font-size:11px;">
      🎯 ORDER BLOCK DETECTED: 10:00 AM Open Range
    </div>
    <div style="font-size:11px; color:#8b949e;">Tap anywhere to close</div>
  </div>
</div>

<script>
var sectors = [
  { name: "AUTO", pct: "+2.87%", type: "bull", y: 20 },
  { name: "LOGISTICS", pct: "+2.41%", type: "bull", y: 58 },
  { name: "CEMENT", pct: "+2.22%", type: "bull", y: 96 },
  { name: "FINANCE", pct: "+1.95%", type: "bull", y: 134 },
  { name: "NBFC", pct: "+1.38%", type: "bull", y: 172 },
  { name: "IT", pct: "+1.14%", type: "bull", y: 210 },
  { name: "INFRA", pct: "+0.85%", type: "bull", y: 248 },
  { name: "PHARMA", pct: "+0.45%", type: "bull", y: 286 },
  { name: "CHEMICAL", pct: "+0.12%", type: "bull", y: 324 },
  { name: "REALTY", pct: "-0.34%", type: "bear", y: 460 },
  { name: "FMCG", pct: "-0.78%", type: "bear", y: 500 },
  { name: "MEDIA", pct: "-1.10%", type: "bear", y: 540 },
  { name: "OIL & GAS", pct: "-1.45%", type: "bear", y: 580 },
  { name: "CONSUMER", pct: "-1.82%", type: "bear", y: 620 },
  { name: "ENERGY", pct: "-2.30%", type: "bear", y: 660 }
];

var cards = [
  { name: "EICHERMOT", sec: "AUTO", pct: "+4.17%", price: "7,058.00", type: "bull", y: 20 },
  { name: "TVSMOTOR", sec: "AUTO", pct: "+2.48%", price: "2,480.00", type: "bull", y: 74 },
  { name: "INOXWIND", sec: "ENERGY", pct: "+6.76%", price: "142.10", type: "bull", y: 128 },
  { name: "TCS", sec: "IT", pct: "+3.92%", price: "4,120.00", type: "bull", y: 182 },
  { name: "AUROPHARMA", sec: "PHARMA", pct: "+2.85%", price: "1,245.00", type: "bull", y: 236 },
  { name: "FEDERALBNK", sec: "FINANCE", pct: "+2.11%", price: "192.50", type: "bull", y: 290 },
  { name: "TATAMOTORS", sec: "AUTO", pct: "+1.95%", price: "965.00", type: "bull", y: 344 },
  { name: "ANANDRATHI", sec: "FINANCE", pct: "-4.68%", price: "2,038.20", type: "bear", y: 530 },
  { name: "MPHASIS", sec: "IT", pct: "-2.14%", price: "2,610.00", type: "bear", y: 584 },
  { name: "COFORGE", sec: "IT", pct: "-1.85%", price: "7,450.00", type: "bear", y: 638 }
];

var container = document.getElementById("nodesContainer");

for (var i = 0; i < sectors.length; i++) {
  var s = sectors[i];
  var div = document.createElement("div");
  div.className = "sec-item";
  div.style.left = "15px";
  div.style.top = s.y + "px";
  div.style.borderColor = s.type === "bull" ? "#1b4d3e" : "#5a1e1e";
  div.innerHTML = "<span>" + s.name + "</span><span style='color:" + (s.type === "bull" ? "#10b981" : "#ef4444") + "'>" + s.pct + "</span>";
  container.appendChild(div);
}

for (var j = 0; j < cards.length; j++) {
  (function(c) {
    var div = document.createElement("div");
    div.className = "stock-card " + c.type;
    div.style.left = "740px";
    div.style.top = c.y + "px";
    div.onclick = function() {
      document.getElementById("popStock").innerText = c.name;
      document.getElementById("popSector").innerText = c.sec + " SECTOR";
      document.getElementById("popPrice").innerText = "₹" + c.price;
      document.getElementById("info-modal").style.display = "flex";
    };
    div.innerHTML = '<div class="card-r1"><span>' + c.name + '</span><span style="color:' + (c.type === "bull" ? "#10b981" : "#ef4444") + '">' + c.pct + '</span></div>' +
                    '<div class="card-r2"><span>₹' + c.price + ' • ' + c.sec + '</span><span style="color:' + (c.type === "bull" ? "#10b981" : "#ef4444") + '">' + (c.type === "bull" ? "LONG BUILD-UP" : "SHORT BUILD-UP") + '</span></div>';
    container.appendChild(div);
  })(cards[j]);
}

var canvas = document.getElementById("flowCanvas");
var ctx = canvas.getContext("2d");
var ladderX = 460;
var inTracks = [];
var outTracks = [];

// Inflow: Bullish UPWARD climb (12 lines per sector), Bearish compressed (4 lines)
for (var i = 0; i < sectors.length; i++) {
  var s = sectors[i];
  if (s.type === "bull") {
    for (var k = 0; k < 12; k++) {
      var targetY = 20 + Math.random() * 340;
      inTracks.push({ p0: [155, s.y + 16], p1: [270, s.y + 16], p2: [370, targetY], p3: [ladderX, targetY], type: "bull" });
    }
  } else {
    for (var k = 0; k < 4; k++) {
      var targetY = 530 + Math.random() * 150;
      inTracks.push({ p0: [155, s.y + 16], p1: [270, s.y + 16], p2: [370, targetY], p3: [ladderX, targetY], type: "bear" });
    }
  }
}

// Outflow to cards
for (var i = 0; i < cards.length; i++) {
  var c = cards[i];
  var count = c.type === "bull" ? 3 : 2;
  for (var k = 0; k < count; k++) {
    var srcY = c.type === "bull" ? 25 + Math.random() * 340 : 535 + Math.random() * 140;
    outTracks.push({ p0: [ladderX + 48, srcY], p1: [560, srcY], p2: [670, c.y + 24], p3: [740, c.y + 24], type: c.type });
  }
}

var inPulses = [];
for (var i = 0; i < inTracks.length; i++) {
  inPulses.push({ trackIndex: i, t: Math.random(), speed: 0.0035 + Math.random() * 0.002, len: 0.14 });
}

var outPulses = [];
for (var i = 0; i < outTracks.length; i++) {
  outPulses.push({ trackIndex: i, t: Math.random(), speed: 0.003 + Math.random() * 0.002, len: 0.16 });
}

function getPoint(p0, p1, p2, p3, t) {
  var u = 1 - t;
  var tt = t * t;
  var uu = u * u;
  var uuu = uu * u;
  var ttt = tt * t;
  return [
    uuu * p0[0] + 3 * uu * t * p1[0] + 3 * u * tt * p2[0] + ttt * p3[0],
    uuu * p0[1] + 3 * uu * t * p1[1] + 3 * u * tt * p2[1] + ttt * p3[1]
  ];
}

function render() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  // 1. Subtle 0.2 tracks
  for (var i = 0; i < inTracks.length; i++) {
    var tr = inTracks[i];
    ctx.beginPath();
    ctx.moveTo(tr.p0[0], tr.p0[1]);
    ctx.bezierCurveTo(tr.p1[0], tr.p1[1], tr.p2[0], tr.p2[1], tr.p3[0], tr.p3[1]);
    ctx.strokeStyle = tr.type === "bull" ? "rgba(16, 185, 129, 0.2)" : "rgba(239, 68, 68, 0.2)";
    ctx.lineWidth = 0.6;
    ctx.stroke();
  }

  for (var i = 0; i < outTracks.length; i++) {
    var tr = outTracks[i];
    ctx.beginPath();
    ctx.moveTo(tr.p0[0], tr.p0[1]);
    ctx.bezierCurveTo(tr.p1[0], tr.p1[1], tr.p2[0], tr.p2[1], tr.p3[0], tr.p3[1]);
    ctx.strokeStyle = tr.type === "bull" ? "rgba(16, 185, 129, 0.2)" : "rgba(239, 68, 68, 0.2)";
    ctx.lineWidth = 0.8;
    ctx.stroke();
  }

  // 2. Ladder ticks
  for (var i = 0; i < 46; i++) {
    var y = 20 + i * 8;
    ctx.beginPath();
    ctx.moveTo(ladderX, y);
    ctx.lineTo(ladderX + 28, y);
    ctx.strokeStyle = "rgba(16, 185, 129, 0.5)";
    ctx.lineWidth = 1.4;
    ctx.stroke();
  }
  for (var i = 0; i < 18; i++) {
    var y = 530 + i * 8.5;
    ctx.beginPath();
    ctx.moveTo(ladderX, y);
    ctx.lineTo(ladderX + 28, y);
    ctx.strokeStyle = "rgba(239, 68, 68, 0.5)";
    ctx.lineWidth = 1.4;
    ctx.stroke();
  }

  // Bracket Boxes
  ctx.strokeStyle = "rgba(56, 139, 253, 0.8)";
  ctx.lineWidth = 2;
  ctx.strokeRect(ladderX + 44, 20, 4, 370);
  ctx.strokeStyle = "rgba(239, 68, 68, 0.8)";
  ctx.strokeRect(ladderX + 44, 530, 4, 155);

  // 3. Moving Comet Pulses
  for (var i = 0; i < inPulses.length; i++) {
    var pt = inPulses[i];
    pt.t += pt.speed;
    if (pt.t > 1) pt.t = 0;
    var tr = inTracks[pt.trackIndex];
    var head = getPoint(tr.p0, tr.p1, tr.p2, tr.p3, pt.t);
    var tail = getPoint(tr.p0, tr.p1, tr.p2, tr.p3, Math.max(0, pt.t - pt.len));

    var grad = ctx.createLinearGradient(tail[0], tail[1], head[0], head[1]);
    grad.addColorStop(0, tr.type === "bull" ? "rgba(16, 185, 129, 0)" : "rgba(239, 68, 68, 0)");
    grad.addColorStop(1, tr.type === "bull" ? "rgba(167, 243, 208, 0.85)" : "rgba(254, 202, 202, 0.85)");
    ctx.beginPath();
    ctx.moveTo(tail[0], tail[1]);
    ctx.lineTo(head[0], head[1]);
    ctx.strokeStyle = grad;
    ctx.lineWidth = 1.0;
    ctx.stroke();
  }

  for (var i = 0; i < outPulses.length; i++) {
    var pt = outPulses[i];
    pt.t += pt.speed;
    if (pt.t > 1) pt.t = 0;
    var tr = outTracks[pt.trackIndex];
    var head = getPoint(tr.p0, tr.p1, tr.p2, tr.p3, pt.t);
    var tail = getPoint(tr.p0, tr.p1, tr.p2, tr.p3, Math.max(0, pt.t - pt.len));

    var grad = ctx.createLinearGradient(tail[0], tail[1], head[0], head[1]);
    grad.addColorStop(0, tr.type === "bull" ? "rgba(16, 185, 129, 0)" : "rgba(239, 68, 68, 0)");
    grad.addColorStop(1, tr.type === "bull" ? "rgba(52, 211, 153, 0.95)" : "rgba(248, 113, 113, 0.95)");
    ctx.beginPath();
    ctx.moveTo(tail[0], tail[1]);
    ctx.lineTo(head[0], head[1]);
    ctx.strokeStyle = grad;
    ctx.lineWidth = 1.2;
    ctx.stroke();
  }

  requestAnimationFrame(render);
}

requestAnimationFrame(render);
</script>
</body>
</html>
"""

components.html(code, height=750, scrolling=True)
