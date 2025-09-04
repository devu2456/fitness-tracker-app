import tkinter as tk
from tkinter import messagebox, ttk
from tkinter import simpledialog
import datetime
import json
import os

class FitnessTrackerApp:
    def __init__(self, master):
        self.master = master
        master.title("ACEestFitness and Gym")

        self.workouts = []
        self.data_file = "workouts.json"
        self.load_workouts()

        # Labels and Entries for adding workouts
        self.workout_label = tk.Label(master, text="Workout:")
        self.workout_label.grid(row=0, column=0, padx=5, pady=5)
        self.workout_entry = tk.Entry(master)
        self.workout_entry.grid(row=0, column=1, padx=5, pady=5)

        self.duration_label = tk.Label(master, text="Duration (minutes):")
        self.duration_label.grid(row=1, column=0, padx=5, pady=5)
        self.duration_entry = tk.Entry(master)
        self.duration_entry.grid(row=1, column=1, padx=5, pady=5)

        self.category_label = tk.Label(master, text="Category:")
        self.category_label.grid(row=2, column=0, padx=5, pady=5)
        self.category_var = tk.StringVar()
        self.category_combo = ttk.Combobox(master, textvariable=self.category_var)
        self.category_combo['values'] = ("Cardio", "Strength", "Flexibility", "Other")
        self.category_combo.grid(row=2, column=1, padx=5, pady=5)
        self.category_combo.current(0)

        self.date_label = tk.Label(master, text="Date:")
        self.date_label.grid(row=3, column=0, padx=5, pady=5)
        self.date_entry = tk.Entry(master)
        self.date_entry.grid(row=3, column=1, padx=5, pady=5)
        self.date_entry.insert(0, datetime.date.today().isoformat())

        # Buttons
        self.add_button = tk.Button(master, text="Add Workout", command=self.add_workout)
        self.add_button.grid(row=4, column=0, columnspan=2, pady=10)

        self.view_button = tk.Button(master, text="View Workouts", command=self.view_workouts)
        self.view_button.grid(row=5, column=0, columnspan=2, pady=5)

        self.delete_button = tk.Button(master, text="Delete Workout", command=self.delete_workout)
        self.delete_button.grid(row=6, column=0, columnspan=2, pady=5)

        self.stats_button = tk.Button(master, text="Show Statistics", command=self.show_stats)
        self.stats_button.grid(row=7, column=0, columnspan=2, pady=5)

        self.save_button = tk.Button(master, text="Save Workouts", command=self.save_workouts)
        self.save_button.grid(row=8, column=0, columnspan=2, pady=5)

        self.load_button = tk.Button(master, text="Load Workouts", command=self.load_workouts)
        self.load_button.grid(row=9, column=0, columnspan=2, pady=5)

    def add_workout(self):
        workout = self.workout_entry.get()
        duration_str = self.duration_entry.get()
        category = self.category_var.get()
        date_str = self.date_entry.get()

        if not workout or not duration_str or not category or not date_str:
            messagebox.showerror("Error", "Please enter all fields.")
            return

        try:
            duration = int(duration_str)
            date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
            self.workouts.append({
                "workout": workout,
                "duration": duration,
                "category": category,
                "date": date_str
            })
            messagebox.showinfo("Success", f"'{workout}' added successfully!")
            self.workout_entry.delete(0, tk.END)
            self.duration_entry.delete(0, tk.END)
            self.date_entry.delete(0, tk.END)
            self.date_entry.insert(0, datetime.date.today().isoformat())
        except ValueError:
            messagebox.showerror("Error", "Duration must be a number and date must be YYYY-MM-DD.")

    def view_workouts(self):
        if not self.workouts:
            messagebox.showinfo("Workouts", "No workouts logged yet.")
            return

        workout_list = "Logged Workouts:\n"
        for i, entry in enumerate(self.workouts):
            workout_list += f"{i+1}. {entry['workout']} - {entry['duration']} min - {entry['category']} - {entry['date']}\n"
        messagebox.showinfo("Workouts", workout_list)

    def delete_workout(self):
        if not self.workouts:
            messagebox.showinfo("Delete", "No workouts to delete.")
            return
        idx = simpledialog.askinteger("Delete Workout", f"Enter workout number to delete (1-{len(self.workouts)}):")
        if idx is None:
            return
        if 1 <= idx <= len(self.workouts):
            removed = self.workouts.pop(idx-1)
            messagebox.showinfo("Deleted", f"Deleted: {removed['workout']} on {removed['date']}")
        else:
            messagebox.showerror("Error", "Invalid workout number.")

    def show_stats(self):
        if not self.workouts:
            messagebox.showinfo("Statistics", "No workouts to show stats.")
            return
        total_workouts = len(self.workouts)
        total_minutes = sum(w["duration"] for w in self.workouts)
        avg_duration = total_minutes / total_workouts if total_workouts else 0
        stats = (
            f"Total Workouts: {total_workouts}\n"
            f"Total Minutes: {total_minutes}\n"
            f"Average Duration: {avg_duration:.2f} min"
        )
        messagebox.showinfo("Statistics", stats)

    def save_workouts(self):
        try:
            with open(self.data_file, "w") as f:
                json.dump(self.workouts, f)
            messagebox.showinfo("Save", "Workouts saved successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save: {e}")

    def load_workouts(self):
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, "r") as f:
                    self.workouts = json.load(f)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = FitnessTrackerApp(root)
    root.mainloop()