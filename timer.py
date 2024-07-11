import tkinter as tk
from tkinter import messagebox
import time

# constants
WORK_MIN = 1
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 15
SESSIONS_BEFORE_LONG_BREAK = 4

#timer class
class PomodoroTimer:
    def __init__(self, root):
        self.root = root
        self.root.title("Pomodoro Timer")
        self.root.geometry("300x200")
        
        self.timer_running = False
        self.sessions_completed = 0
        self.timer_seconds = WORK_MIN * 60
        
        self.label = tk.Label(root, text="Pomodoro Timer", font=("Helvetica", 18))
        self.label.pack(pady=20)
        
        self.time_label = tk.Label(root, text=self.format_time(self.timer_seconds), font=("Helvetica", 48))
        self.time_label.pack(pady=20)
        
        self.start_button = tk.Button(root, text="Start", command=self.start_timer)
        self.start_button.pack(side="left", padx=20)
        
        self.reset_button = tk.Button(root, text="Reset", command=self.reset_timer)
        self.reset_button.pack(side="right", padx=20)
    
    def start_timer(self):
        if not self.timer_running:
            self.timer_running = True
            self.update_timer()
    
    def reset_timer(self):
        self.timer_running = False
        self.sessions_completed = 0
        self.timer_seconds = WORK_MIN * 60
        self.time_label.config(text=self.format_time(self.timer_seconds))
    
    def update_timer(self):
        if self.timer_running:
            if self.timer_seconds > 0:
                self.timer_seconds -= 1
                self.time_label.config(text=self.format_time(self.timer_seconds))
                self.root.after(1000, self.update_timer)
            else:
                self.sessions_completed += 1
                if self.sessions_completed % (SESSIONS_BEFORE_LONG_BREAK + 1) == 0:
                    self.timer_seconds = LONG_BREAK_MIN * 60
                    messagebox.showinfo("Break Time!")
                elif self.sessions_completed % 2 == 0:
                    self.timer_seconds = SHORT_BREAK_MIN * 60
                    messagebox.showinfo("Break Time!")
                else:
                    self.timer_seconds = WORK_MIN * 60
                    messagebox.showinfo("Work Time")
                self.update_timer()
    
