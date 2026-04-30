import paho.mqtt.client as mqtt
import json
import time
import math
import random
from datetime import datetime

client = mqtt.Client()
client.connect("localhost", 1883, 60)

# Startvärden
soil = 75.0

while True:
    now = datetime.now()

    # -------------------------
    # Simulera tid på dagen
    # -------------------------
    hour = now.hour + now.minute / 60

    # Temperatur: dag/natt sinuskurva
    temp = 22 + 6 * math.sin((hour / 24) * 2 * math.pi)

    # Lite naturligt brus
    temp += random.uniform(-0.5, 0.5)

    # -------------------------
    # Soil moisture
    # -------------------------
    soil -= random.uniform(0.1, 0.4)   # torkar långsamt

    # Simulera vattning om torrt
    if soil < 25:
        soil = random.uniform(70, 85)

    soil = round(soil, 1)

    # -------------------------
    # Humidity
    # Omvänd relation mot temp
    # -------------------------
    humidity = 75 - (temp - 20) * 2 + random.uniform(-3, 3)

    humidity = max(30, min(95, humidity))

    payload = {
        "timestamp": now.isoformat(),
        "soil": soil,
        "temp": round(temp, 1),
        "humidity": round(humidity, 1)
    }

    client.publish("greenhouse/sensor1", json.dumps(payload))

    print("Sent:", payload)

    time.sleep(5)