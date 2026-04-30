import subprocess
import sys
import time
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]

def run_process(cmd, name):
    print(f"Starting {name}...")
    return subprocess.Popen(cmd, cwd=BASE_DIR)

if __name__ == "__main__":
    processes = []

    # 1. MQTT listener
    processes.append(run_process(
    [sys.executable, "-m", "backend.mqtt.listener"],
    "MQTT Listener"
    ))


    # 2. Flask app
    processes.append(run_process(
        [sys.executable, "-m", "backend.dashboard.app"],
        "Flask Dashboard"
    ))

    # 3. Simulator
    processes.append(run_process(
        [sys.executable, "simulator/simulator.py"],
        "Simulator"
    ))

    print("\nAll services started.\nPress CTRL+C to stop everything.\n")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping services...")

        for p in processes:
            p.terminate()

        print("All stopped.")