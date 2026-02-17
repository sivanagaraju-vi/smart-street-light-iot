from flask import Flask, render_template
import sqlite3
import os

app = Flask(__name__)

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
        return "No Data Available"

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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
