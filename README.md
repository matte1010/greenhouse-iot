# 🌱 Greenhouse IoT Monitoring System

An end-to-end IoT system for monitoring greenhouse environmental conditions using ESP32 (or simulator), MQTT communication, and a Python-based backend with real-time visualization.

---

## 📌 Overview

This project simulates and implements a full IoT pipeline for greenhouse monitoring:

- ESP32 (or Python simulator) generates sensor data
- MQTT broker handles real-time messaging
- Python backend processes and stores data
- Flask dashboard visualizes live and historical data

---

## 📡 System Architecture

ESP32 / Simulator → MQTT Broker → Python Listener → CSV Storage → Flask Dashboard

---

## 🌡️ Monitored Parameters

- Soil moisture (%)
- Temperature (°C)
- Humidity (%)

---

## 🧰 Tech Stack

- Python (MQTT client, backend, dashboard)
- ESP32 (Arduino / PlatformIO)
- Mosquitto MQTT broker
- Flask (web dashboard)
- Pandas (data handling)
- Plotly (visualization)

---

## 🚀 Features

- Real-time sensor data streaming via MQTT
- Persistent data logging (CSV)
- Live dashboard with latest readings
- Historical trend visualization
- Modular architecture (simulator or real hardware)

---

## 📁 Project Structure

backend/        # MQTT listener + dashboard  
esp32/          # Firmware (PlatformIO)  
simulator/      # Test data generator  
data/           # Stored logs  
docs/           # Documentation  

---

## ▶️ Running the Project

### 1. Start MQTT broker
```bash
brew services start mosquitto
```

### 2. Start listener
```bash
python backend/mqtt/listener.py
```

### 3. Run simulator (optional)
```bash
python simulator/simulator.py
```

### 4. Start dashboard
```bash
python backend/dashboard/app.py
```

Open:
```
http://127.0.0.1:5000
```

---

## 🔌 Future ESP32 Setup

ESP32 will replace the simulator and publish real sensor data via MQTT.

---

## 📊 Future Improvements

- Real-time WebSocket dashboard
- Alert system for soil moisture thresholds
- Database storage (SQLite / InfluxDB)
- Mobile-friendly UI
- Power optimization for ESP32

---

## 👤 Author

Mathias Olsson  