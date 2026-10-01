import json
import tkinter as tk
from tkinter import ttk, messagebox

from stack_engine import find_short_circuit


class PCBVisualizer:
    def __init__(self, root, board):
        self.root = root
        self.root.title("Smart Circuit & PCB Trace Short-Circuit Finder")
        self.root.geometry("900x700")

        self.board = board
        self.cell_size = 32
        self.canvas = tk.Canvas(root, width=700, height=700, bg="white")
        self.canvas.pack(padx=10, pady=10)

        self.status_var = tk.StringVar()
        self.status_var.set("Ready to simulate")

        ttk.Label(root, textvariable=self.status_var, font=("Arial", 12, "bold")).pack(pady=5)

        self.frame = ttk.Frame(root)
        self.frame.pack(pady=5)

        self.run_button = ttk.Button(self.frame, text="Start Simulation", command=self.run_simulation)
        self.run_button.pack(side=tk.LEFT, padx=5)

        self.reset_button = ttk.Button(self.frame, text="Reset Board", command=self.reset_board)
        self.reset_button.pack(side=tk.LEFT, padx=5)

        self.result = None
        self.path = []
        self.current_index = 0
        self.animation_id = None

        self.draw_board()

    def color_for_cell(self, value):
        if value == 0:
            return "black"
        elif value == 1:
            return "green"
        elif value == 2:
            return "red"
        return "white"

    def draw_board(self):
        self.canvas.delete("all")

        rows = len(self.board)
        cols = len(self.board[0])

        for r in range(rows):
            for c in range(cols):
                x1 = c * self.cell_size
                y1 = r * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size

                color = self.color_for_cell(self.board[r][c])
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="gray", width=1)

        self.canvas.config(width=cols * self.cell_size, height=rows * self.cell_size)

    def reset_board(self):
        if self.animation_id:
            self.root.after_cancel(self.animation_id)
            self.animation_id = None

        self.current_index = 0
        self.path = []
        self.status_var.set("Board reset")
        self.draw_board()

    def run_simulation(self):
        if self.animation_id:
            self.root.after_cancel(self.animation_id)
            self.animation_id = None

        self.result = find_short_circuit(self.board, start=(0, 0))
        self.path = self.result["path"]
        self.current_index = 0

        if self.result["short_detected"]:
            self.status_var.set(f"Short circuit detected at {self.result['position']}")
        else:
            self.status_var.set("No short circuit found. Trace is safe.")

        self.animate_path()

    def animate_path(self):
        if self.current_index < len(self.path):
            row, col = self.path[self.current_index]
            self.highlight_cell(row, col)
            self.current_index += 1
            self.animation_id = self.root.after(300, self.animate_path)
        else:
            self.status_var.set(
                "Simulation finished. "
                + ("Short circuit detected." if self.result["short_detected"] else "No short circuit found.")
            )
            self.animation_id = None

    def highlight_cell(self, row, col):
        self.canvas.delete("highlight")

        x1 = col * self.cell_size
        y1 = row * self.cell_size
        x2 = x1 + self.cell_size
        y2 = y1 + self.cell_size

        self.canvas.create_rectangle(
            x1 + 3,
            y1 + 3,
            x2 - 3,
            y2 - 3,
            fill="yellow",
            outline="blue",
            width=2,
            tags="highlight"
        )


def load_board(path):
    with open(path, "r") as file:
        return json.load(file)


def main():
    # Use a default test board
    board = load_board("test_boards/short_board.json")

    root = tk.Tk()
    PCBVisualizer(root, board)
    root.mainloop()


if __name__ == "__main__":
    main()
