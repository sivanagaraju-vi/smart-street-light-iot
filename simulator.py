import random
import time
from datetime import datetime
import sqlite3
from database import init_db

init_db()

while True:
    now = datetime.now()
    hour = now.hour

    if hour >= 18 or hour <= 6:
        status = "ON"
        traffic = random.randint(0, 20)

        if traffic < 5:
            brightness = 30
        elif traffic < 15:
            brightness = 60
        else:
            brightness = 100

        energy = 100 * (brightness / 100)
    else:
        status = "OFF"
        traffic = 0
        brightness = 0
        energy = 0

    fault = random.choice([0]*19 + [1])

    conn = sqlite3.connect("streetlight.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO streetlight
        (timestamp, status, traffic, brightness, energy, fault)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (str(now), status, traffic, brightness, energy, fault))

    conn.commit()
    conn.close()

    print("Logged:", status, brightness, energy)
    time.sleep(5)
