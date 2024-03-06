import time
import tkinter as tk
import threading
from tkinter import ttk
import datetime
import json
import matplotlib.pyplot as plt


class CountdownApp:
    def __init__(self, root):
        self.root = root
        self.style = ttk.Style()
        self.root.title("Countdown application")
        self.root.configure(background="lightgreen")
        self.root.resizable(False, False)
        self.root.attributes("-topmost", True)
        self.minutes = tk.IntVar(value=24)
        self.seconds = tk.IntVar(value=59)
        self.paused = False
        self.running = False
        self.interapted_counter = 0
        self.finished_counter = 0
        self.total_time_counter = 0
        self.time_label = tk.Label(
            root, text="00:00", font=("Helvetica", 24), bg="lightgreen"
        )
        self.time_label.pack(pady=20)

        self.interupted_label = tk.Label(
            root, text="Interupted:", font=("Halvetica, 10"), bg="lightgreen"
        )
        self.interupted_value = tk.Label(
            root, text="0", font=("Helvetica, 10"), bg="lightgreen"
        )
        self.interupted_label.pack()
        self.interupted_value.pack()
        self.finished_label = tk.Label(
            root, text="Finished:", font=("Halvetica, 10"), bg="lightgreen"
        )
        self.finished_value = tk.Label(
            root, text="0", font=("Helvetica, 10"), bg="lightgreen"
        )
        self.total_time_label = tk.Label(
            root, text="Total time:", font=("Halvetica, 10"), bg="lightgreen"
        )
        self.total_time_value = tk.Label(
            root, text="00:00", font=("Halvetica, 10"), bg="lightgreen"
        )
        self.finished_label.pack()
        self.finished_value.pack()
        self.total_time_label.pack()
        self.total_time_value.pack()
        self.minutes_entry = ttk.Entry(
            root,
            textvariable=self.minutes,
            validate="key",
            validatecommand=(root.register(
                self.validate_numeric_minutes_input), "%P"),
        )
        self.minutes_entry.pack(pady=5)
        self.seconds_entry = ttk.Entry(
            root,
            textvariable=self.seconds,
            validate="key",
            validatecommand=(root.register(
                self.validate_numeric_seconds_input), "%P"),
        )
        self.seconds_entry.pack(pady=5)
        self.style.configure(
            "Green.TButton",
            **self.getBtnStyle("#4CAF50"),
        )
        self.style.configure(
            "Blue.TButton",
            **self.getBtnStyle("#7c7cf9"),
        )
        self.style.configure(
            "Red.TButton",
            **self.getBtnStyle("#eb4040"),
        )
        self.style.map("Green.TButton", background=[("active", "#071803")])
        self.style.map("Red.TButton", background=[("active", "#630909")])
        self.style.map("Blue.TButton", background=[("active", "#150561")])
        self.startButton = ttk.Button(
            root,
            text="Start",
            style="Green.TButton",
            command=self.start_countdown,
            width=4,
        )
        self.startButton.pack(side=tk.LEFT, padx=4)
        self.stop_button = ttk.Button(
            root, text="Stop", style="Red.TButton", command=self.stop_countdown, width=4
        )
        self.stop_button.pack(side=tk.LEFT, padx=4)
        self.pause_button = ttk.Button(
            root,
            text="Pause",
            style="Blue.TButton",
            command=self.pause_countdown,
            width=5,
        )
        self.pause_button.pack(side=tk.LEFT, padx=5)
        self.style.configure(
            "Report.TButton",
            **self.getBtnStyle("#33FFF3"),
        )
        self.style.map("Report.TButton", background=[("active", "#339993")])
        self.reportButton = ttk.Button(
            root,
            text="R",
            style="Report.TButton",
            command=self.start_report,
            width=2,
        )
        self.reportButton.pack(side=tk.LEFT, padx=4)

    def validate_numeric_seconds_input(self, seconds) -> bool:
        if (
            seconds.isdigit()
            and int(seconds) <= 60
            and int(seconds) >= 0
            or seconds == ""
        ):
            return True
        else:
            return False

    def validate_numeric_minutes_input(self, minutes) -> bool:
        if minutes.isdigit() or minutes == "":
            return True
        else:
            return False

    def update_time_label(self):
        minutes_or_zero = self.minutes_entry.get()
        seconds_or_zero = self.seconds_entry.get()
        if minutes_or_zero == "":
            minutes_or_zero = 0
        if seconds_or_zero == "":
            seconds_or_zero = 0
        seconds = int(seconds_or_zero) + (int(minutes_or_zero) * 60)
        while seconds >= 0 and not self.stop_thread:
            if self.running and not self.paused:
                min, sec = divmod(seconds, 60)
                if min >= 1:
                    self.time_label.config(text=f"{min:02d}:{sec:02d}")
                else:
                    self.time_label.config(text=f"00:{sec:02d}")
                time.sleep(1)
                seconds -= 1
        if not self.stop_thread:
            self.running = False
            self.time_label.config(text="Time's up!")
            self.change_screen_colour()
            self.finished_counter += 1
            self.finished_value.config(text=self.finished_counter)
            self.total_time_counter += int(seconds_or_zero) + (
                int(minutes_or_zero) * 60
            )
            min, sec = divmod(self.total_time_counter, 60)
            if min >= 1:
                self.total_time_value.config(text=f"{min:02d}:{sec:02d}")
            else:
                self.total_time_value.config(text=f"00:{sec:02d}")

    def change_screen_colour(self):
        for i in range(5):
            self.root.configure(background="red")
            self.time_label.config(background="red")
            self.interupted_label.configure(background="red")
            self.interupted_value.configure(background="red")
            self.finished_label.configure(background="red")
            self.finished_value.configure(background="red")
            self.total_time_value.configure(background="red")
            self.total_time_label.configure(background="red")
            self.root.update()
            self.root.after(1000)
            self.root.configure(background="lightgreen")
            self.time_label.config(background="lightgreen")
            self.interupted_label.configure(background="lightgreen")
            self.interupted_value.configure(background="lightgreen")
            self.finished_label.configure(background="lightgreen")
            self.finished_value.configure(background="lightgreen")
            self.total_time_value.configure(background="lightgreen")
            self.total_time_label.configure(background="lightgreen")
            self.root.update()
            self.root.after(1000)

    def start_countdown(self):
        if not self.running and not self.paused:
            self.style.configure(
                "Blue.TButton",
                **self.getBtnStyle("#7c7cf9"),
            )

            self.running = True
            self.paused = False
            self.stop_thread = False
            threading.Thread(target=self.update_time_label).start()

    def stop_countdown(self):
        self.running = False
        self.paused = False
        self.stop_thread = True
        self.time_label.config(text="00:00")
        self.interapted_counter += 1
        self.interupted_value.config(text=self.interapted_counter)

    def pause_countdown(self):
        if self.running and ("Time's up!" not in self.time_label.cget("text")):
            self.paused = not self.paused
            if self.paused:
                self.time_label.config(text="Paused!")
                self.style.configure(
                    "Blue.TButton",
                    **self.getBtnStyle("#000000"),
                )
            else:
                self.style.configure(
                    "Blue.TButton",
                    **self.getBtnStyle("#7c7cf9"),
                )

    def start_report(self):
        x_line = []
        y_line = []
        try:
            with open("data.json", "r") as file:
                try:
                    json_file = json.load(file)
                except json.decoder.JSONDecodeError:
                    json_file = []

        except FileNotFoundError:
            with open("data.json", "w") as file:
                json.dump([], file, indent=4)
                json_file = []

        for data in json_file:
            x_line.append(data["date_time"])
            y_line.append(data["total_time_counter"])

        plt.plot(x_line, y_line)

        plt.xlabel("Dates")
        plt.ylabel("Time in seconds")
        plt.title("Countdown application chart")

        plt.xticks(rotation=90)
        plt.tight_layout()
        plt.show()

    def getBtnStyle(self, background):
        return {
            "background": background,  # Blue background
            "foreground": "white",  # White text
            "borderwidth": 0,  # No border
            "font": ("Helvetica", 12),
            "relief": "flat",  # Flat relief
            "padding": 10,
        }


def on_closing(app):
    data = {
        "date_time": str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M")),
        "interapted_counter": app.interapted_counter,
        "finished_counter": app.finished_counter,
        "total_time_counter": app.total_time_counter,
    }

    try:
        with open("data.json", "r") as file:
            try:
                existing_data = json.load(file)
            except json.decoder.JSONDecodeError:
                existing_data = []
    except FileNotFoundError:
        existing_data = []

    existing_data.append(data)

    with open("data.json", "w") as file:
        json.dump(existing_data, file, indent=4)
    app.root.destroy()


def main():
    root = tk.Tk()
    root.title("Countdown")
    window_width = 260
    window_height = 350
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")
    app = CountdownApp(root)
    root.protocol("WM_DELETE_WINDOW", lambda: on_closing(app))
    root.mainloop()


if __name__ == "__main__":
    main()
