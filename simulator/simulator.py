import random
import time
import json
import paho.mqtt.client as mqtt

client = mqtt.Client()
client.connect("localhost", 1883, 60)

while True:
    data = {
        "soil": random.randint(20, 80),
        "temp": round(random.uniform(15, 30), 1),
        "humidity": random.randint(40, 90)
    }

    client.publish("greenhouse/sensor1", json.dumps(data))
    print("Sent:", data)

    time.sleep(5)