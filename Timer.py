import tkinter as tk

class PomodoroApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Pomodoro Timer")
        self.root.geometry("420x250")
        self.root.configure(bg="white")

        # Canvas
        self.canvas = tk.Canvas(root, width=580, height=400, bg="white", highlightthickness=0)
        self.canvas.pack(pady=10)

        # --- Big rounded rectangle background ---
        self.rounded_rect(20, 20, 400, 150, 40, fill="#d9e6f2", outline="#7d8fa0", width=4)

        # --- Play circle ---
        self.button_circle = self.canvas.create_oval(50, 40, 120, 110, fill="white", outline="#7d8fa0", width=3)

        # Play symbol
        self.play_symbol = self.canvas.create_polygon(
            75, 60, 75, 90, 105, 75,
            fill="#334155", tags="symbol"
        )

        # Text inside the player
        self.label_text = self.canvas.create_text(
            150, 75, text="Now playing:\nStudy mode",
            font=("Calibri", 22, "bold"), fill="#334155", anchor="w"
        )
        

        # Timer
        self.time_text = self.canvas.create_text(
            350, 100, text="25:00", font=("Calibri", 10, "bold"), fill="#334155", anchor="w"
        )

        # Progress bar
        self.progress_line = self.canvas.create_line(50, 130, 370, 130, fill="#7d8fa0", width=4, capstyle="round")
        self.progress_knob = self.canvas.create_oval(50, 125, 60, 135, fill="white", outline="#7d8fa0", width=2)

        # Buttons
        self.new_session_rect = self.rounded_rect(20, 170, 205, 215, 20,
                                                  fill="#7d8fa0", outline="#7d8fa0", width=0, tags="new_session")
        self.new_session_text = self.canvas.create_text(110, 193, text="New study session",
                                                        font=("Arial", 12, "bold"), fill="white", tags="new_session")

        self.break_rect = self.rounded_rect(215, 170, 400, 215, 20,
                                            fill="#7d8fa0", outline="#7d8fa0", width=0, tags="break_timer")
        self.break_text = self.canvas.create_text(305, 193, text="Break timer",
                                                  font=("Arial", 12, "bold"), fill="white", tags="break_timer")

        self.canvas.itemconfigure(self.new_session_rect, state="normal")
        self.canvas.itemconfigure(self.new_session_text, state="normal")
        self.canvas.itemconfigure(self.break_rect, state="normal")
        self.canvas.itemconfigure(self.break_text, state="normal")

        self.canvas.tag_bind(self.button_circle, "<Button-1>", self.toggle_timer)
        self.canvas.tag_bind("symbol", "<Button-1>", self.toggle_timer)
        self.canvas.tag_bind("new_session", "<Button-1>", self.reset_session)
        self.canvas.tag_bind("break_timer", "<Button-1>", self.start_break)

        # Timer vars
        self.total_time = 25 * 60
        self.time_left = self.total_time
        self.break_time = 5 * 60
        self.running = False
        self.after_id = None

    def rounded_rect(self, x1, y1, x2, y2, r, **kwargs):
        points = [
            x1+r, y1, x2-r, y1, x2, y1,
            x2, y1+r, x2, y2-r, x2, y2,
            x2-r, y2, x1+r, y2, x1, y2,
            x1, y2-r, x1, y1+r, x1, y1
        ]
        return self.canvas.create_polygon(points, smooth=True, **kwargs)

    def toggle_timer(self, event=None):
        if not self.running:
            self.running = True
            self.show_pause_symbol()
            self.countdown()
        else:
            self.running = False
            self.show_play_symbol()
            if self.after_id:
                self.root.after_cancel(self.after_id)
                self.after_id = None

    def show_play_symbol(self):
        self.canvas.delete("pause_symbol")
        self.canvas.delete("symbol")
        self.play_symbol = self.canvas.create_polygon(
            75, 60, 75, 90, 105, 75,
            fill="#334155", tags="symbol"
        )
        self.canvas.tag_bind("symbol", "<Button-1>", self.toggle_timer)

    def show_pause_symbol(self):
        self.canvas.delete("symbol")
        left_bar = self.canvas.create_rectangle(70, 60, 80, 90,
                                                fill="#334155", outline="#334155", tags="pause_symbol")
        right_bar = self.canvas.create_rectangle(90, 60, 100, 90,
                                                 fill="#334155", outline="#334155", tags="pause_symbol")
        self.canvas.tag_bind("pause_symbol", "<Button-1>", self.toggle_timer)

    def countdown(self):
        if self.running and self.time_left > 0:
            mins, secs = divmod(self.time_left, 60)
            self.canvas.itemconfig(self.time_text, text=f"{mins:02d}:{secs:02d}")

            progress_ratio = 1 - (self.time_left / self.total_time)
            knob_x = 55 + progress_ratio * (370 - 50)
            self.canvas.coords(self.progress_knob, knob_x-5, 125, knob_x+5, 135)

            self.time_left -= 1
            self.after_id = self.root.after(1000, self.countdown)
        elif self.time_left == 0:
            self.canvas.itemconfig(self.time_text, text="00:00")
            self.show_play_symbol()
            self.running = False
            self.canvas.itemconfig(self.label_text, text="Time's up!")

    def reset_session(self, event=None):
        if self.after_id:
            self.root.after_cancel(self.after_id)
        self.time_left = self.total_time
        self.running = False
        self.show_play_symbol()
        self.canvas.itemconfig(self.time_text, text="25:00")
        self.canvas.itemconfig(self.label_text, text="Now playing:\nStudy mode")
        self.canvas.coords(self.progress_knob, 50, 125, 60, 135)
        self.canvas.itemconfig(self.break_message, text="")
        

    def start_break(self, event=None):
        if self.after_id:
            self.root.after_cancel(self.after_id)
        self.time_left = self.break_time
        self.running = False
        self.show_play_symbol()
        self.canvas.itemconfig(self.time_text, text="05:00")
        self.canvas.coords(self.progress_knob, 50, 125, 60, 135)
        self.canvas.itemconfig(self.label_text, text="Break time!")
        if self.time_left == 0:
            self.canvas.itemconfig(self.time_text, text="00:00")
            self.show_play_symbol()
            self.running = False
            self.canvas.itemconfig(self.label_text, text="Break is over! \n Ready to study?")


# --- Run ---
if __name__ == "__main__":
    root = tk.Tk()
    app = PomodoroApp(root)
    root.mainloop()
