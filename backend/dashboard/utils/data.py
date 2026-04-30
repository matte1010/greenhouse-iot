import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
csv_file = BASE_DIR / "storage" / "data_log.csv"


def get_latest_data():
    df = pd.read_csv(csv_file)
    latest = df.tail(1).iloc[0]

    return {
        "soil": float(latest["soil"]),
        "temp": float(latest["temperature"]),
        "humidity": float(latest["humidity"])
    }


def get_history_data():
    df = pd.read_csv(csv_file)

    return {
        "soil": df["soil"].tolist(),
        "temperature": df["temperature"].tolist(),
        "humidity": df["humidity"].tolist()
    }