import paho.mqtt.client as mqtt
import json
from datetime import datetime
from backend.common.data import insert_sensor_data

# -----------------------
# Config
# -----------------------
BROKER = "localhost"
PORT = 1883
TOPIC = "greenhouse/#"


# -----------------------
# MQTT callback
# -----------------------
def on_message(client, userdata, msg):
    try:
        payload = msg.payload.decode("utf-8")
        data = json.loads(payload)

        print("Received:", data)

        insert_sensor_data(
            data.get("soil"),
            data.get("temp"),
            data.get("humidity")
        )

    except Exception as e:
        print("Error:", e)


# -----------------------
# MQTT setup
# -----------------------
client = mqtt.Client()
client.on_message = on_message

client.connect(BROKER, PORT, 60)
client.subscribe(TOPIC)

print(f"Listening on topic: {TOPIC}")

client.loop_forever()