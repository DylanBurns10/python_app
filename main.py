import os
import tkinter as tk
from tkinter import messagebox
import psutil
import time
from datetime import timedelta

LOG_FILE = "habits.json"

def log_executables():
    current_time = time.time()
    with open(LOG_FILE, "a") as log:
        try:
            log.write(f"\n--- Log at {time.strftime('%Y-%m-%d %H:%M:%S')} ---\n")
        except Exception as e:
            print(f"Error: {e}")
        for process in psutil.process_iter(['pid', 'name', 'create_time']):
            try:
                create_time = process.info.get('create_time', current_time)
                process_uptime = current_time - create_time
                uptime = str(timedelta(seconds=process_uptime))
                #print(f"Process: {process.info['name']} (PID: {process.info['pid']})")
                #print(f"  Uptime: {uptime}")
                if os.stat(LOG_FILE).st_size == 0:
                    if process.info['name'] != "svchost.exe":
                        log.write(f"{process.info['name']}\n")
                        log.write(f"  Uptime: {uptime}\n")
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue

def main():
    log_executables()    
main()