import random
import threading
import time

live = {"temperature": None, "humidity": None, "wind": None}
running = {"on": False}

def sensor_loop(key, low, high):
    while running["on"]:
        value = round(random.uniform(low, high), 1)
        if key == "temperature" and random.randint(1, 12) == 1:
            value = -99
        live[key] = value
        time.sleep(1)

def start(temp_low, temp_high):
    running["on"] = True
    jobs = [("temperature", temp_low, temp_high), ("humidity", 20, 80), ("wind", 5, 35)]
    for job in jobs:
        thread = threading.Thread(target=sensor_loop, args=job, daemon=True)
        thread.start()

def stop():
    running["on"] = False
