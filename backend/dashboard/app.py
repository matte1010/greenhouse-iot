from flask import Flask, render_template_string
import pandas as pd
from pathlib import Path
import plotly.express as px

app = Flask(__name__)

BASE_DIR = Path(__file__).resolve().parent.parent
csv_file = BASE_DIR / "storage" / "data_log.csv"


HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Greenhouse Dashboard</title>
    <meta http-equiv="refresh" content="5">
    <style>
        body { font-family: Arial; margin: 40px; }
        .box { padding: 20px; border: 1px solid #ddd; margin-bottom: 20px; }
        h1 { color: #2c3e50; }
    </style>
</head>
<body>

<h1>🌱 Greenhouse IoT Dashboard</h1>

<div class="box">
    <h2>Latest Sensor Values</h2>
    <p><b>Soil:</b> {{ soil }}</p>
    <p><b>Temperature:</b> {{ temp }}</p>
    <p><b>Humidity:</b> {{ humidity }}</p>
</div>

<div class="box">
    <h2>Last 10 readings</h2>
    <pre>{{ table }}</pre>
</div>

</body>
</html>
"""


@app.route("/")
def index():
    if not csv_file.exists():
        return "No data yet"

    df = pd.read_csv(csv_file)

    latest = df.tail(1).iloc[0]

    fig = px.line(df, y="soil", title="Soil Moisture Over Time")
    graph_html = fig.to_html(full_html=False)

    return f"""
    <html>
    <head>
        <title>Greenhouse Dashboard</title>
        <meta http-equiv="refresh" content="5">
    </head>
    <body>
        <h1>🌱 Greenhouse IoT Dashboard</h1>

        <h2>Latest</h2>
        <p>Soil: {latest['soil']}</p>
        <p>Temp: {latest['temperature']}</p>
        <p>Humidity: {latest['humidity']}</p>

        <h2>Soil trend</h2>
        {graph_html}
    </body>
    </html>
    """


if __name__ == "__main__":
    app.run(debug=True, port=5000)