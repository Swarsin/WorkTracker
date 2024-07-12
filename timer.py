import tkinter as tk
from tkinter import messagebox
import time

# change later to allow user to change these things
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 15
SESSIONS_BEFORE_LONG_BREAK = 4

class PomodoroTimer:
    def __init__(self, root):
        #window variables
        self.root = root
        self.root.title("Habit Tracker")
        self.root.geometry("300x250")

        self.timer_running = False
        self.sessions_completed = 0
        self.timer_seconds = WORK_MIN * 60

        #create a Label in the window - above the timer
        self.label = tk.Label(root, text=f"Pomodoro Timer, Session {self.sessions_completed + 1}", font=("Helvetica", 18))
        self.label.pack(pady=20)
        
        #create timer
        self.timer_label = tk.Label(root, text=self.format_time(self.timer_seconds), font=("Helvetica", 48))
        self.timer_label.pack(pady=20)
        
        #create start button
        self.start_button = tk.Button(root, text="Start", command=self.start_timer)
        self.start_button.pack(side="left", padx=20)
        
        #create reset button
        self.reset_button = tk.Button(root, text="Reset", command=self.reset_timer)
        self.reset_button.pack(side="right", padx=20)
    
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
                if self.sessions_completed % (SESSIONS_BEFORE_LONG_BREAK + 1) == 0:
                    self.timer_seconds = LONG_BREAK_MIN * 60
                    messagebox.showinfo("Break Time", "Take a long break!")
                elif self.sessions_completed % 2 == 0:
                    self.timer_seconds = SHORT_BREAK_MIN * 60
                    messagebox.showinfo("Break Time", "Take a short break!")
                else:
                    self.timer_seconds = WORK_MIN * 60
                    messagebox.showinfo("Work Time", "Back to work!")
                self.update_timer()
    
    def reset_timer(self):
        self.timer_running = False
        self.sessions_completed = 0
        self.timer_seconds = WORK_MIN * 60
        self.timer_label.config(text=self.format_time(self.timer_seconds))
    
    def format_time(self, seconds):
        minutes = seconds // 60
        seconds = seconds % 60
        return f"{minutes:02d}:{seconds:02d}"

if __name__ == "__main__":
    root = tk.Tk()
    app = PomodoroTimer(root)
    root.mainloop()
