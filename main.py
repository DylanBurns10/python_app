from datetime import timedelta
import psutil
import time
import os
import tkinter as tk
from tkinter import ttk
from ttkbootstrap import Style
from ttkbootstrap.constants import *

LOG_FILE = "habits.txt"

def load_txt():
    if not os.path.exists(LOG_FILE):
        return []
    with open(LOG_FILE, 'r') as file:
        content = file.readlines()
    return [line.strip() for line in content]

def create_scrollable_frame(mainPage):
    # Create a Canvas widget to hold the scrollable frame
    canvas = tk.Canvas(mainPage)
    scrollbar = ttk.Scrollbar(mainPage, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)

    # Create a frame inside the canvas that will hold the content
    scrollable_frame = ttk.Frame(canvas)

    # Create a window on the canvas to contain the scrollable frame
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

    # Place the scrollbar next to the canvas
    scrollbar.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)

    # Update scroll region whenever the content changes (important for scrolling)
    def on_frame_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    # Bind the on_frame_configure to update the scroll region whenever the frame is resized
    scrollable_frame.bind("<Configure>", on_frame_configure)

    # Bind the mouse wheel event to the canvas
    def on_mouse_wheel(event):
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    canvas.bind_all("<MouseWheel>", on_mouse_wheel)

    return scrollable_frame

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
                rounded_uptime = round(process_uptime, 2)

                # Create a timedelta object from seconds
                uptime_timedelta = timedelta(seconds=rounded_uptime)

                # Extract days, hours, minutes, and seconds
                days = uptime_timedelta.days
                hours, remainder = divmod(uptime_timedelta.seconds, 3600)
                minutes, seconds = divmod(remainder, 60)

                # Format the uptime as "X days, Y hours, Z minutes, W seconds"
                formatted_uptime = f"{days} days, {hours} hours, {minutes} minutes, {seconds} seconds"

                if os.stat(LOG_FILE).st_size == 0:
                    if process.info['name'] != "svchost.exe":
                        log.write(f"{process.info['name']}\n")
                        log.write(f"  Uptime: {formatted_uptime}\n")

            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue

def main():
    log_executables()
    root = tk.Tk()
    root.title("Viewer")
    style = Style(theme='darkly')
    # Create a parent frame for the canvas and scrollbar
    mainPage = ttk.Frame(root)
    mainPage.pack(fill="both", expand=True)

    # Create a scrollable frame inside the parent frame
    scrollable_frame = create_scrollable_frame(mainPage)
    data = load_txt()

    # Add key-value pairs to the scrollable frame
    for line in data:
        # Create labels for each line
        line_label = ttk.Label(scrollable_frame, text=line, anchor="w", width=60)
        line_label.grid(row=len(scrollable_frame.winfo_children()), column=0, padx=10, pady=5)

    #b1 = ttk.Button(mainPage, text="Button 1", bootstyle=SUCCESS)
    #b1.pack(side=LEFT, padx=5, pady=10)
    
    #b2 = ttk.Button(mainPage, text="Button 2", bootstyle=SUCCESS)
    #b2.pack(side=RIGHT, padx=5, pady=10)
    # Start the Tkinter main loop
    root.mainloop()
    
main()