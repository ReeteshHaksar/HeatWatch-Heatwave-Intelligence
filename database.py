import random
import sqlite3
from datetime import datetime

from alerts import get_alert

DB_PATH = __file__.replace("database.py", "heatwatch.db")
COLUMNS = "id, station_id, city, temperature, humidity, wind, alert_level, reviewed, time"
connection = sqlite3.connect(DB_PATH)

def setup(stations):
    connection.execute("CREATE TABLE IF NOT EXISTS stations (station_id TEXT PRIMARY KEY, city TEXT, type TEXT, latitude REAL, longitude REAL)")
    connection.execute("CREATE TABLE IF NOT EXISTS readings (id INTEGER PRIMARY KEY AUTOINCREMENT, station_id TEXT, city TEXT, temperature REAL, humidity REAL, wind REAL, condition TEXT, alert_level TEXT, reviewed TEXT DEFAULT 'No', time TEXT)")
    count = connection.execute("SELECT COUNT(*) FROM stations").fetchone()[0]
    if count > 0:
        return
    for station in stations:
        row = (station.station_id, station.city, station.kind, station.info[2], station.info[3])
        connection.execute("INSERT INTO stations VALUES (?, ?, ?, ?, ?)", row)
    random.seed(7)
    for number in range(50):
        station = random.choice(stations)
        if station.kind == "plains":
            temp = round(random.uniform(34, 48), 1)
        else:
            temp = round(random.uniform(30, 41), 1)
        alert = get_alert(temp, station.threshold, station.city)
        insert_reading(station.station_id, station.city, temp, random.randint(20, 80), random.randint(5, 35), "Sunny", alert.level)
    random.seed()

def insert_reading(station_id, city, temperature, humidity, wind, condition, alert_level):
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    sql = "INSERT INTO readings (station_id, city, temperature, humidity, wind, condition, alert_level, time) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
    connection.execute(sql, (station_id, city, temperature, humidity, wind, condition, alert_level, now))
    connection.commit()

def all_readings():
    return connection.execute("SELECT " + COLUMNS + " FROM readings ORDER BY id DESC").fetchall()

def heatwave_readings():
    return connection.execute("SELECT " + COLUMNS + " FROM readings WHERE alert_level != 'Normal' ORDER BY id DESC").fetchall()

def hottest_readings():
    return connection.execute("SELECT " + COLUMNS + " FROM readings ORDER BY temperature DESC LIMIT 10").fetchall()

def search_city(text):
    return connection.execute("SELECT " + COLUMNS + " FROM readings WHERE city LIKE ? ORDER BY id DESC", ("%" + text + "%",)).fetchall()

def average_per_city():
    return connection.execute("SELECT city, ROUND(AVG(temperature), 1) FROM readings GROUP BY city ORDER BY city").fetchall()

def count_per_level():
    return connection.execute("SELECT alert_level, COUNT(*) FROM readings GROUP BY alert_level").fetchall()

def heatwaves_per_city():
    return connection.execute("SELECT city, COUNT(*) FROM readings WHERE alert_level != 'Normal' GROUP BY city ORDER BY COUNT(*) DESC").fetchall()

def overview_numbers():
    totals = connection.execute("SELECT COUNT(*), MAX(temperature) FROM readings").fetchone()
    heat = connection.execute("SELECT COUNT(*), COUNT(DISTINCT city) FROM readings WHERE alert_level != 'Normal'").fetchone()
    hottest = connection.execute("SELECT city FROM readings ORDER BY temperature DESC LIMIT 1").fetchone()
    if hottest is None:
        return (0, 0, 0, 0, "no data yet")
    return (totals[0], heat[0], heat[1], totals[1], hottest[0])

def mark_reviewed(reading_id):
    connection.execute("UPDATE readings SET reviewed = 'Yes' WHERE id = ?", (reading_id,))
    connection.commit()

def delete_reading(reading_id):
    connection.execute("DELETE FROM readings WHERE id = ?", (reading_id,))
    connection.commit()
