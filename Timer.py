import tkinter as tk

class PomodoroApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Pomodoro Timer")
        self.root.geometry("500x400")
        self.root.configure(bg="white")

        # --- Canvas for everything ---
        self.canvas = tk.Canvas(root, width=460, height=280, bg="white", highlightthickness=0)
        self.canvas.pack(pady=20)

        # Rounded rectangle background
        self.rounded_rect(10, 10, 450, 210, 30, fill="#d9e6f2", outline="#7d8fa0", width=4)

        # Circle button (centered at 230,85)
        self.button_circle = self.canvas.create_oval(185, 40, 275, 130, fill="white", outline="#7d8fa0", width=3)

        # Play symbol (triangle centered)
        self.play_symbol = self.canvas.create_polygon(
            220, 60, 220, 110, 255, 85,
            fill="#7d8fa0", tags="symbol"
        )

        # Progress bar line
        self.progress_line = self.canvas.create_line(80, 170, 380, 170, fill="#7d8fa0", width=4, capstyle="round")
        self.progress_knob = self.canvas.create_oval(75, 165, 85, 175, fill="white", outline="#7d8fa0", width=2)

        # Time labels
        self.left_time = self.canvas.create_text(60, 170, text="25:00", font=("Calibri", 12), fill="#333", anchor="e")
        self.right_time = self.canvas.create_text(400, 170, text="25:00", font=("Calibri", 12), fill="#333", anchor="w")

        # Break message (hidden at first)
        self.break_message = self.canvas.create_text(230, 240, text="", font=("Calibri", 14, "bold"), fill="#7d8fa0")

        # Custom "New Session" button (hidden at first)
        self.new_session_rect = self.rounded_rect(150, 260, 310, 310, 20,
                                                  fill="#7d8fa0", outline="#7d8fa0", width=0, tags="new_session")
        self.new_session_text = self.canvas.create_text(230, 285, text="New Session",
                                                        font=("Arial", 12, "bold"), fill="white", tags="new_session")

        # Hide button initially
        self.canvas.itemconfigure(self.new_session_rect, state="hidden")
        self.canvas.itemconfigure(self.new_session_text, state="hidden")

        # Bind button clicks
        self.canvas.tag_bind(self.button_circle, "<Button-1>", self.toggle_timer)
        self.canvas.tag_bind("symbol", "<Button-1>", self.toggle_timer)
        self.canvas.tag_bind("new_session", "<Button-1>", self.reset_session)

        # Timer variables
        self.total_time = 25 * 60
        self.time_left = self.total_time
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

    def capsule(self, x1, y1, x2, y2, fill, tag):
        r = (x2 - x1) / 2
        self.canvas.create_oval(x1, y1, x1+2*r, y2, fill=fill, outline=fill, tags=tag)
        self.canvas.create_oval(x2-2*r, y1, x2, y2, fill=fill, outline=fill, tags=tag)
        self.canvas.create_rectangle(x1+r, y1, x2-r, y2, fill=fill, outline=fill, tags=tag)

    def toggle_timer(self, event=None):
        if not self.running:  # Start or resume
            self.running = True
            self.update_button("pause")
            self.countdown()
        else:  # Pause
            self.running = False
            self.update_button("play")
            if self.after_id:
                self.root.after_cancel(self.after_id)
                self.after_id = None

    def update_button(self, state):
        self.canvas.delete("symbol")
        if state == "play":
            self.play_symbol = self.canvas.create_polygon(
                220, 60, 220, 110, 255, 85,
                fill="#7d8fa0", tags="symbol"
            )
        else:
            self.capsule(210, 60, 225, 110, "#7d8fa0", "symbol")
            self.capsule(235, 60, 250, 110, "#7d8fa0", "symbol")

        self.canvas.tag_bind("symbol", "<Button-1>", self.toggle_timer)

    def countdown(self):
        if self.running and self.time_left > 0:
            mins, secs = divmod(self.time_left, 60)
            self.canvas.itemconfig(self.left_time, text=f"{mins:02d}:{secs:02d}")

            progress_ratio = 1 - (self.time_left / self.total_time)
            knob_x = 80 + progress_ratio * (380 - 80)
            self.canvas.coords(self.progress_knob, knob_x-5, 165, knob_x+5, 175)

            self.time_left -= 1
            self.after_id = self.root.after(1000, self.countdown)
        elif self.time_left == 0:
            self.canvas.itemconfig(self.left_time, text="00:00")
            self.update_button("play")
            self.running = False
            self.canvas.itemconfig(self.break_message, text="Take a well-deserved break!")
            self.canvas.itemconfigure(self.new_session_rect, state="normal")
            self.canvas.itemconfigure(self.new_session_text, state="normal")

    def reset_session(self, event=None):
        """Reset timer to 25 minutes."""
        if self.after_id:
            self.root.after_cancel(self.after_id)
        self.time_left = self.total_time
        self.running = False
        self.update_button("play")
        self.canvas.itemconfig(self.left_time, text="25:00")
        self.canvas.coords(self.progress_knob, 75, 165, 85, 175)
        self.canvas.itemconfig(self.break_message, text="")
        self.canvas.itemconfigure(self.new_session_rect, state="hidden")
        self.canvas.itemconfigure(self.new_session_text, state="hidden")


# --- Run ---
if __name__ == "__main__":
    root = tk.Tk()
    app = PomodoroApp(root)
    root.mainloop()
