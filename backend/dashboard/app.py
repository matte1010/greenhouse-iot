from flask import Flask, jsonify
import pandas as pd
from pathlib import Path

app = Flask(__name__)

BASE_DIR = Path(__file__).resolve().parent.parent
csv_file = BASE_DIR / "storage" / "data_log.csv"


# -----------------------
# API (latest data)
# -----------------------
@app.route("/api/latest")
def api_latest():
    df = pd.read_csv(csv_file)
    latest = df.tail(1).iloc[0]

    return jsonify({
        "soil": float(latest["soil"]),
        "temp": float(latest["temperature"]),
        "humidity": float(latest["humidity"])
    })


# -----------------------
# API (history data)
# -----------------------
@app.route("/api/history")
def history():
    df = pd.read_csv(csv_file)
    return df.to_dict(orient="list")


# -----------------------
# Dashboard UI
# -----------------------
@app.route("/")
def index():
    return """
<!DOCTYPE html>
<html>
<head>
    <title>Greenhouse Dashboard</title>
    <style>
        body { font-family: Arial; margin: 40px; }
        .card { padding: 20px; border: 1px solid #ddd; margin-bottom: 10px; }
        .status { font-size: 20px; font-weight: bold; }
    </style>
</head>

<body>
    <h1>🌱 Greenhouse IoT Dashboard</h1>

    <div class="card">
        <div>Soil: <span id="soil"></span></div>
        <div>Temp: <span id="temp"></span></div>
        <div>Humidity: <span id="humidity"></span></div>
    </div>

    <div class="card status" id="status"></div>

    <div class="card">
        <h3>🌱 Soil Moisture</h3>
        <div id="soilGraph"></div>
    </div>

    <div class="card">
        <h3>🌡️ Temperature</h3>
        <div id="tempGraph"></div>
    </div>

    <div class="card">
        <h3>💧 Humidity</h3>
        <div id="humidityGraph"></div>
    </div>

<script src="https://cdn.plot.ly/plotly-latest.min.js"></script>

<script>

// --------------------
// LIVE DATA
// --------------------
async function fetchData() {
    const res = await fetch("/api/latest");
    const data = await res.json();

    document.getElementById("soil").innerText = data.soil;
    document.getElementById("temp").innerText = data.temp;
    document.getElementById("humidity").innerText = data.humidity;

    // Alerts
    let status = "OK";
    let color = "green";

    if (data.soil < 30) {
        status = "⚠️ Water needed";
        color = "red";
    }
    if (data.temp > 30) {
        status = "🔥 Too hot";
        color = "red";
    }
    if (data.humidity < 40) {
        status = "🌫️ Dry air";
        color = "orange";
    }

    const el = document.getElementById("status");
    el.innerText = status;
    el.style.color = color;
}


// --------------------
// GRAPHS
// --------------------
async function loadGraphs() {
    const res = await fetch("/api/history");
    const data = await res.json();

    const x = Array.from({length: data.soil.length}, (_, i) => i);

    // Soil + threshold
    Plotly.newPlot("soilGraph", [
        {
            x: x,
            y: data.soil,
            type: "scatter",
            name: "Soil"
        },
        {
            x: x,
            y: Array(x.length).fill(30),
            type: "scatter",
            name: "Threshold",
            line: {dash: "dash"}
        }
    ]);

    // Temperature
    Plotly.newPlot("tempGraph", [
        {
            x: x,
            y: data.temperature,
            type: "scatter",
            name: "Temp"
        }
    ]);

    // Humidity
    Plotly.newPlot("humidityGraph", [
        {
            x: x,
            y: data.humidity,
            type: "scatter",
            name: "Humidity"
        }
    ]);
}


// --------------------
// LOOP
// --------------------
setInterval(fetchData, 2000);

fetchData();
loadGraphs();

</script>

</body>
</html>
"""


if __name__ == "__main__":
    app.run(debug=True, port=5000)