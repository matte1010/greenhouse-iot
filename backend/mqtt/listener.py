import paho.mqtt.client as mqtt
import json
import csv
from datetime import datetime
from pathlib import Path

# -----------------------
# Config
# -----------------------
BROKER = "localhost"
PORT = 1883
TOPIC = "greenhouse/#"

# -----------------------
# Storage setup
# -----------------------
BASE_DIR = Path(__file__).resolve().parent.parent
storage_dir = BASE_DIR / "storage"
storage_dir.mkdir(exist_ok=True)

csv_file = storage_dir / "data_log.csv"

# Create CSV header if file is empty
if not csv_file.exists() or csv_file.stat().st_size == 0:
    with open(csv_file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp", "soil", "temperature", "humidity"])


# -----------------------
# Save function
# -----------------------
def save_to_csv(data):
    with open(csv_file, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            datetime.now().isoformat(),
            data.get("soil"),
            data.get("temp"),
            data.get("humidity")
        ])


# -----------------------
# MQTT callback
# -----------------------
def on_message(client, userdata, msg):
    try:
        payload = msg.payload.decode("utf-8")
        data = json.loads(payload)

        print("Received:", data)

        save_to_csv(data)

    except json.JSONDecodeError:
        print("Invalid JSON received:", msg.payload)

    except Exception as e:
        print("Error processing message:", e)


# -----------------------
# MQTT setup
# -----------------------
client = mqtt.Client()
client.on_message = on_message

client.connect(BROKER, PORT, 60)
client.subscribe(TOPIC)

print(f"Listening on topic: {TOPIC}")

client.loop_forever()