from backend.common.db import get_connection


def insert_sensor_data(soil, temp, humidity):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO sensor_data (soil, temperature, humidity)
        VALUES (?, ?, ?)
    """, (soil, temp, humidity))

    conn.commit()
    conn.close()


def get_latest_data():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT soil, temperature, humidity
        FROM sensor_data
        ORDER BY id DESC
        LIMIT 1
    """)

    row = cursor.fetchone()
    conn.close()

    if row:
        return {
            "soil": row["soil"],
            "temp": row["temperature"],
            "humidity": row["humidity"]
        }

    return {
        "soil": 0,
        "temp": 0,
        "humidity": 0
    }


def get_history_data():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT timestamp, soil, temperature, humidity
        FROM sensor_data
        ORDER BY id ASC
    """)

    rows = cursor.fetchall()
    conn.close()

    return {
        "time": [row["timestamp"] for row in rows],
        "soil": [row["soil"] for row in rows],
        "temperature": [row["temperature"] for row in rows],
        "humidity": [row["humidity"] for row in rows]
    }