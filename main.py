import json
import os
import datetime
import tkinter as tk
from tkinter import messagebox

DATA_FILE = "habits.json"

# Load habits from JSON file
def load_habits():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    return {}

# Save habits to JSON file
def save_habits(habits):
    with open(DATA_FILE, "w") as file:
        json.dump(habits, file, indent=4)

# Add new habit
def add_habit():
    habit_name = entry_habit.get()
    if habit_name:
        habits = load_habits()
        if habit_name not in habits:
            habits[habit_name] = []
            save_habits(habits)
            listbox_habits.insert(tk.END, habit_name)
            entry_habit.delete(0, tk.END)
        else:
            messagebox.showinfo("Error", "Habit already exists!")

# Log habit for today
def log_habit():
    selected = listbox_habits.curselection()
    if not selected:
        messagebox.showinfo("Error", "Select a habit first!")
        return

    habit_name = listbox_habits.get(selected[0])
    habits = load_habits()
    today = datetime.date.today().strftime("%Y-%m-%d")
    
    if today not in habits[habit_name]:
        habits[habit_name].append(today)
        save_habits(habits)
        messagebox.showinfo("Success", f"Habit '{habit_name}' logged for today!")
    else:
        messagebox.showinfo("Info", "Habit already logged today!")

# View progress
def view_progress():
    habits = load_habits()
    progress_text = ""
    
    for habit, dates in habits.items():
        progress_text += f"{habit}: {len(dates)} days logged\n"

    messagebox.showinfo("Progress", progress_text if progress_text else "No habits tracked yet.")

# GUI Setup
root = tk.Tk()
root.title("Habit Tracker")

frame = tk.Frame(root)
frame.pack(pady=10)

entry_habit = tk.Entry(frame, width=30)
entry_habit.grid(row=0, column=0, padx=5)

btn_add = tk.Button(frame, text="Add Habit", command=add_habit)
btn_add.grid(row=0, column=1)

listbox_habits = tk.Listbox(root, width=40, height=10)
listbox_habits.pack(pady=10)

btn_log = tk.Button(root, text="Log Habit", command=log_habit)
btn_log.pack(pady=5)

btn_progress = tk.Button(root, text="View Progress", command=view_progress)
btn_progress.pack(pady=5)

# Load existing habits
habits = load_habits()
for habit in habits:
    listbox_habits.insert(tk.END, habit)

root.mainloop()
