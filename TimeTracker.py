import time
import tkinter as tk
from tkinter import messagebox, filedialog
import pandas as pd
from datetime import datetime, timedelta

class TimeTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Time Tracker")

        # Variables
        self.check_in_time = None
        self.check_out_time = None
        self.pause_start_time = None
        self.total_pause_duration = timedelta(0)
        self.is_paused = False
        self.save_location = "time_log.xlsx"  # Default save location

        # UI Elements
        self.check_in_button = tk.Button(root, text="Check In", command=self.check_in, width=15)
        self.check_in_button.pack(pady=5)

        self.pause_button = tk.Button(root, text="Pause", command=self.pause, state="disabled", width=15)
        self.pause_button.pack(pady=5)

        self.end_button = tk.Button(root, text="End", command=self.end_session, state="disabled", width=15)
        self.end_button.pack(pady=5)

        self.set_location_button = tk.Button(root, text="Set Save Location", command=self.set_save_location, width=15)
        self.set_location_button.pack(pady=5)

        self.location_label = tk.Label(root, text=f"Save Location: {self.save_location}", wraplength=400, justify="left")
        self.location_label.pack(pady=5)

    def check_in(self):
        self.check_in_time = datetime.now()
        self.check_in_button.config(state="disabled")
        self.pause_button.config(state="normal")
        self.end_button.config(state="normal")
        messagebox.showinfo("Checked In", f"Checked in at {self.check_in_time.strftime('%H:%M:%S')}")

    def pause(self):
        if not self.is_paused:
            # Start pause
            self.pause_start_time = datetime.now()
            self.is_paused = True
            self.pause_button.config(text="Resume")
            messagebox.showinfo("Paused", "Session paused.")
        else:
            # Resume
            pause_duration = datetime.now() - self.pause_start_time
            self.total_pause_duration += pause_duration
            self.is_paused = False
            self.pause_button.config(text="Pause")
            messagebox.showinfo("Resumed", "Session resumed.")

    def end_session(self):
        if self.is_paused:
            messagebox.showerror("Error", "Resume before ending the session.")
            return

        self.check_out_time = datetime.now()
        total_time = self.check_out_time - self.check_in_time
        working_time = total_time - self.total_pause_duration

        # Log data
        log_data = {
            "Date": self.check_in_time.date(),
            "Day": self.check_in_time.strftime("%A"),
            "Check-In Time": self.check_in_time.strftime("%H:%M:%S"),
            "Check-Out Time": self.check_out_time.strftime("%H:%M:%S"),
            "Total Time (hours)": round(total_time.total_seconds() / 3600, 2),
            "Pause Time (hours)": round(self.total_pause_duration.total_seconds() / 3600, 2),
            "Working Time (hours)": round(working_time.total_seconds() / 3600, 2),
        }

        # Save to Excel/CSV
        try:
            df = pd.read_excel(self.save_location)
        except FileNotFoundError:
            df = pd.DataFrame(columns=log_data.keys())

        df = pd.concat([df, pd.DataFrame([log_data])], ignore_index=True)
        df.to_excel(self.save_location, index=False)
        messagebox.showinfo("Session Ended", f"Session logged and saved to {self.save_location}.")

        # Reset app
        self.reset_session()

    def set_save_location(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel Files", "*.xlsx"), ("All Files", "*.*")],
            title="Choose Save Location"
        )
        if file_path:
            self.save_location = file_path
            self.location_label.config(text=f"Save Location: {self.save_location}")
            messagebox.showinfo("Save Location Set", f"Logs will now be saved to: {self.save_location}")

    def reset_session(self):
        self.check_in_button.config(state="normal")
        self.pause_button.config(state="disabled", text="Pause")
        self.end_button.config(state="disabled")
        self.check_in_time = None
        self.check_out_time = None
        self.pause_start_time = None
        self.total_pause_duration = timedelta(0)
        self.is_paused = False


# Run the app
if __name__ == "__main__":
    time.sleep(0.5)
    root = tk.Tk()
    app = TimeTrackerApp(root)
    root.mainloop()