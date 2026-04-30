from flask import Flask, jsonify, render_template
from backend.common.db import init_db
from backend.common.data import get_latest_data, get_history_data

app = Flask(__name__)

init_db()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/latest")
def latest():
    return jsonify(get_latest_data())


@app.route("/api/history")
def history():
    return jsonify(get_history_data())


if __name__ == "__main__":
    app.run(debug=True, port=5000)