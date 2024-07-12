import tkinter as tk
from tkinter import messagebox
#from tkinter import ttk
import time

# change later to allow user to change these things
work_min = 25
short_break_min = 5
long_break_min = 15
sessions_before_long_break = 4

class ChangeTimingWindow(tk.Toplevel):
    def __init__(self):
        super.__init__()
        self.title("Change Session Timings")
        self.geometry("300x400")
        
        #add work textbox
        work_label = tk.Label(self, "Work Duration: ")
        work_label.grid(row=0, column=0, padx=10, pady=10, sticky="e")
        work_entry = tk.Entry(self, width=30)
        work_entry.grid(row=0, column=1, padx=10, pady=10)
        
        #add short break textbox
        short_break_label = tk.Label(self, "Short Break Duration: ")
        short_break_label.grid(row=1, column=0, padx=10, pady=10, sticky="e")
        short_break_entry = tk.Entry(self, width=30)
        short_break_entry.grid(row=1, column=1, padx=10, pady=10)

        #add long break textbox
        long_break_label = tk.Label(self, "Long Break Duration: ")
        long_break_label.grid(row=2, column=0, padx=10, pady=10, sticky="e")
        long_break_entry = tk.Entry(self, width=30)
        long_break_entry.grid(row=2, column=1, padx=10, pady=10)

        #add short break textbox
        sessions_before_long_break_label = tk.Label(self, "Sessions Before Long Break: ")
        sessions_before_long_break_label.grid(row=3, column=0, padx=10, pady=10, sticky="e")
        sessions_before_long_break_entry = tk.Entry(self, width=30)
        sessions_before_long_break_entry.grid(row=3, column=1, padx=10, pady=10)

    def getAllContents(self):
        entry = work_entry.get()
        


class PomodoroTimer:
    def __init__(self, root):
        #window variables
        self.root = root
        self.root.title("Habit Tracker")
        self.root.geometry("300x250")

        self.timer_running = False
        self.sessions_completed = 0
        self.timer_seconds = work_min * 60

        #create a Label in the window - above the timer
        self.label = tk.Label(root, text=f"Pomodoro Timer, Session {self.sessions_completed + 1}", font=("Helvetica", 18))
        self.label.pack(pady=20)
        
        #create timer
        self.timer_label = tk.Label(root, text=self.format_time(self.timer_seconds), font=("Helvetica", 48))
        self.timer_label.pack(pady=20)
        
        #create start button
        self.start_button = tk.Button(root, text="Start", command=self.start_timer)
        self.start_button.pack(side="left", padx=20)

        #create button to open sessions timings window
        self.change_timing_button = tk.Button(root, text="Change Timing", command=self.open_window)
        self.change_timing_button.pack(side="bottom")
        
        #create reset button
        self.reset_button = tk.Button(root, text="Reset", command=self.reset_timer)
        self.reset_button.pack(side="right", padx=20)
    
    def open_window(self):
        pass

    def start_timer(self):
        if not self.timer_running:
            self.timer_running = True
            self.update_timer()

    def update_timer(self):
        if self.timer_running:
            if self.timer_seconds > 0:
                self.timer_seconds -= 1
                self.timer_label.config(text=self.format_time(self.timer_seconds))
                self.root.after(1000, self.update_timer)
            else: #check over this again i dont really understand what the hell this is doing
                self.sessions_completed += 1
                if self.sessions_completed % (sessions_before_long_break + 1) == 0:
                    self.timer_seconds = long_break_min * 60
                    messagebox.showinfo("Break Time", "Take a long break!")
                elif self.sessions_completed % 2 == 0:
                    self.timer_seconds = short_break_min * 60
                    messagebox.showinfo("Break Time", "Take a short break!")
                else:
                    self.timer_seconds = work_min * 60
                    messagebox.showinfo("Work Time", "Back to work!")
                self.update_timer()
    
    def reset_timer(self):
        self.timer_running = False
        self.sessions_completed = 0
        self.timer_seconds = work_min * 60
        self.timer_label.config(text=self.format_time(self.timer_seconds))
    
    def format_time(self, seconds):
        minutes = seconds // 60
        seconds = seconds % 60
        return f"{minutes:02d}:{seconds:02d}"

if __name__ == "__main__":
    root = tk.Tk()
    app = PomodoroTimer(root)
    root.mainloop()
