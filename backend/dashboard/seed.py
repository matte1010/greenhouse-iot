from backend.common.db import init_db
from backend.common.data import insert_sensor_data
import random

init_db()

for _ in range(20):
    insert_sensor_data(
        random.randint(20, 70),
        random.randint(18, 32),
        random.randint(35, 80)
    )

print("Done")