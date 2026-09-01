import sqlite3
from datetime import datetime

DB_NAME = "food_waste_history.db"


def create_database():
    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            food_type TEXT,
            guests INTEGER,
            quantity REAL,
            predicted_waste REAL,
            risk TEXT,
            suggested_quantity REAL,
            cost_saving REAL
        )
    """)

    conn.commit()
    conn.close()


def save_prediction(
    food_type,
    guests,
    quantity,
    predicted_waste,
    risk,
    suggested_quantity,
    cost_saving
):
    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO predictions (
            date,
            food_type,
            guests,
            quantity,
            predicted_waste,
            risk,
            suggested_quantity,
            cost_saving
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        datetime.now().strftime("%Y-%m-%d %H:%M"),
        food_type,
        guests,
        quantity,
        predicted_waste,
        risk,
        suggested_quantity,
        cost_saving
    ))

    conn.commit()
    conn.close()


def get_history():
    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            date,
            food_type,
            guests,
            quantity,
            predicted_waste,
            risk,
            suggested_quantity,
            cost_saving
        FROM predictions
        ORDER BY id DESC
    """)

    rows = cursor.fetchall()

    conn.close()

    return rows


def clear_history():
    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("DELETE FROM predictions")

    conn.commit()
    conn.close()