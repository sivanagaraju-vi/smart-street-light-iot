import sqlite3

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
