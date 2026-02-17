from flask import Flask, render_template
import sqlite3
import os
import random
import time
from datetime import datetime
import threading

app = Flask(__name__)

# -------- DATABASE INIT --------
def init_db():
    conn = sqlite3.connect("streetlight.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS streetlight (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            status TEXT,
            traffic INTEGER,
            brightness INTEGER,
            energy REAL,
            fault INTEGER
        )
    """)

    conn.commit()
    conn.close()

# -------- AUTO DATA GENERATOR --------
def generate_data():
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

        time.sleep(5)

# -------- FETCH DATA --------
def get_data():
    conn = sqlite3.connect("streetlight.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM streetlight ORDER BY id DESC LIMIT 20")
    rows = cursor.fetchall()
    conn.close()

    return rows[::-1]

@app.route("/")
def dashboard():
    rows = get_data()

    if not rows:
        return "Generating Data... Please refresh in 5 seconds."

    latest = rows[-1]

    total_energy = sum([row[5] for row in rows])
    total_faults = sum([row[6] for row in rows])
    energy_list = [row[5] for row in rows]

    return render_template("index.html",
                           status=latest[2],
                           traffic=latest[3],
                           brightness=latest[4],
                           energy=latest[5],
                           total_energy=round(total_energy,2),
                           faults=total_faults,
                           energy_list=energy_list)

# -------- START SYSTEM IMMEDIATELY (IMPORTANT FIX) --------
init_db()

thread = threading.Thread(target=generate_data)
thread.daemon = True
thread.start()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

