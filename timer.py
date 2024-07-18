import tkinter as tk
from tkinter import messagebox
from datetime import date
from connect_to_sheets import update_sheet

work_min = 25
short_break_min = 5
long_break_min = 15
work_goal = ""
time_goal = 0
work_done = ""
distractions = ""
future_improvements = ""

class SetGoalWindow(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.title("Set Goal")
        self.geometry("350x200")

        #add work goal textbox
        work_goal_label = tk.Label(self, text="Work Goal: ")
        work_goal_label.grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.work_goal_entry = tk.Entry(self, width=20)
        self.work_goal_entry.grid(row=0, column=1, padx=10, pady=10)

        #add time goal textbox
        time_goal_label = tk.Label(self, text="Time Goal (in hrs): ")
        time_goal_label.grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.time_goal_entry = tk.Entry(self, width=20)
        self.time_goal_entry.grid(row=1, column=1, padx=10, pady=10)

        submit_button = tk.Button(self, text="Submit", command=self.submit)
        submit_button.grid(row=2, column=1, padx=10, pady=10)

    def submit(self):
        work_goal = self.work_goal_entry.get()
        time_goal = int(self.time_goal_entry.get())
        #print(work_goal + str(time_goal))
        self.destroy()

class ChangeTimingWindow(tk.Toplevel):
    def __init__(self, pomdoro_timer):
        super().__init__()
        self.title("Change Session Timings")
        self.geometry("350x200")
        self.pomodoro_timer = pomdoro_timer

        # Add work textbox
        work_label = tk.Label(self, text="Work Duration: ")
        work_label.grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.work_entry = tk.Entry(self, width=20)
        self.work_entry.grid(row=0, column=1, padx=10, pady=10)

        # Add short break textbox
        short_break_label = tk.Label(self, text="Short Break Duration: ")
        short_break_label.grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.short_break_entry = tk.Entry(self, width=20)
        self.short_break_entry.grid(row=1, column=1, padx=10, pady=10)

        # Add long break textbox
        long_break_label = tk.Label(self, text="Long Break Duration: ")
        long_break_label.grid(row=2, column=0, padx=10, pady=10, sticky="e")
        self.long_break_entry = tk.Entry(self, width=20)
        self.long_break_entry.grid(row=2, column=1, padx=10, pady=10)

        # Add change button
        submit_button = tk.Button(self, text="Change", command=self.submit)
        submit_button.grid(row=4, column=1, padx=10, pady=10)

    def submit(self): #REMEMBER TO ADD VALIDATION SO THAT USER CANT ENTER STUPID SHIT
        global work_min, short_break_min, long_break_min
        work_min = int(self.work_entry.get())
        short_break_min = int(self.short_break_entry.get())
        long_break_min = int(self.long_break_entry.get())
        #print(work_min, short_break_min, long_break_min)

        self.pomodoro_timer.update_timer_labels()
        self.destroy()

class EndSessionWindow(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.title = "End Session"
        self.geometry("350x200")

        #add work done textbox:
        work_done_label = tk.Label(self, text="Work done this session: ")
        work_done_label.grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.work_done_entry = tk.Entry(self, width=20)
        self.work_done_entry.grid(row=0, column=1, padx=10, pady=10)

        #add future improvements textbox:
        future_improvements_label = tk.Label(self, text="Future Improvements: ")
        future_improvements_label.grid(row=1, column=0, padx=10, pady=10)
        self.future_improvements_entry = tk.Entry(self, width=20)
        self.future_improvements_entry.grid(row=1, column=1, padx=10, pady=10)

        #add distractions textbox:
        distractions_label = tk.Label(self, text="Distractions: ")
        distractions_label.grid(row=2, column=0, padx=10, pady=10)
        self.distractions_entry = tk.Entry(self, width=20)
        self.distractions_entry.grid(row=2, column=1, padx=10, pady=10)

        submit_button = tk.Button(self, text="Submit", command=self.submit)
        submit_button.grid(row=3, column=1, padx=10, pady=10)

    def submit(self):
        work_done = self.work_done_entry.get()
        future_improvements = self.future_improvements_entry.get()
        distractions = self.distractions_entry.get()
        #print(work_done, future_improvements, distractions)
        update_sheet([str(date.today()), work_goal, work_done, "Hours Worked", "Goal Met?", future_improvements, distractions])
        self.destroy()

class PomodoroTimer:
    def __init__(self, root):
        # window variables
        self.root = root
        self.root.title("Habit Tracker")
        self.root.geometry("300x325")

        self.timer_running = False
        self.sessions_completed = 0
        self.timer_seconds = work_min * 60
        self.current_event = "Work!"

        # create a Label in the window - above the timer
        self.label = tk.Label(root, text=f"Pomodoro Timer | {self.current_event}", font=("Helvetica", 18))
        self.label.pack(pady=20)

        # create timer
        self.timer_label = tk.Label(root, text=self.format_time(self.timer_seconds), font=("Helvetica", 48))
        self.timer_label.pack(pady=20)

        # create frame for buttons
        button_frame = tk.Frame(root)
        button_frame.pack(pady=20, fill='x')

        # create start button
        self.start_button = tk.Button(button_frame, text="Start", command=self.start_timer)
        self.start_button.pack(side="left", padx=10)

        # create reset button
        self.reset_button = tk.Button(button_frame, text="Reset", command=self.reset_timer)
        self.reset_button.pack(side="right", padx=10)

        # create button to open sessions timings window
        self.change_timing_button = tk.Button(button_frame, text="Change Timing", command=self.open_window)
        self.change_timing_button.pack(side="bottom")

        #create button to open set goal window
        self.goal_button = tk.Button(button_frame, text="Set Goal", command=self.open_goal_window)
        self.goal_button.pack(side="bottom", padx=10, pady=10)

        #create button to open end window
        self.end_button = tk.Button(button_frame, text="End Sessions", command=self.open_end_sessions_window)
        self.end_button.pack(side="bottom")

    def open_goal_window(self):
        goal_window = SetGoalWindow()
        goal_window.mainloop()

    def update_timer_labels(self):
        self.timer_seconds = work_min * 60
        self.timer_label.config(text=self.format_time(self.timer_seconds))

        self.label.config(text=f"Pomodoro Timer | {self.current_event}")

    def open_window(self):
        #global change_timing_window
        change_timing_window = ChangeTimingWindow(app)
        change_timing_window.mainloop()
        self.update_timer_labels()

    def open_end_sessions_window(self):
        end_sessions_window = EndSessionWindow()
        end_sessions_window.mainloop()
        #NEED TO PUT SOMETHING HERE???

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
            else: #need to redo this part - it's not as i want it currently
                self.sessions_completed += 1
                if self.sessions_completed % 8 == 0:
                    self.timer_seconds = long_break_min * 60
                    messagebox.showinfo("Break Time", "Take a long break!")
                    self.current_event = "Long Break!"
                elif self.sessions_completed % 2 == 1:
                    self.timer_seconds = short_break_min * 60
                    messagebox.showinfo("Break Time", "Take a short break!")
                    self.current_event = "Short Break!"
                else:
                    self.timer_seconds = work_min * 60
                    messagebox.showinfo("Work Time", "Back to work!")
                    self.current_event = "Work!"
                self.update_timer()
                self.update_timer_labels()

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
