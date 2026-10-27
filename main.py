import random
import tkinter as tk
from tkinter import ttk, messagebox
from stack_engine import find_short_circuit

class PCBVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("TraceStack: Advanced PCB Fault Isolation System")
        
        self.rows = 6
        self.cols = 6
        self.cell_size = 50
        
        # Dynamically size canvas to fit grid perfectly
        canvas_width = self.cols * self.cell_size
        canvas_height = self.rows * self.cell_size
        
        self.canvas = tk.Canvas(root, width=canvas_width, height=canvas_height, bg="#111")
        self.canvas.pack(padx=15, pady=15)

        self.status_var = tk.StringVar()
        self.status_var.set("Ready. Fully randomized circuit layout loaded.")

        ttk.Label(root, textvariable=self.status_var, font=("Arial", 12, "bold")).pack(pady=5)

        self.frame = ttk.Frame(root)
        self.frame.pack(pady=10)

        self.run_button = ttk.Button(self.frame, text="Start Full Trace Audit", command=self.run_simulation)
        self.run_button.pack(side=tk.LEFT, padx=5)

        self.reset_button = ttk.Button(self.frame, text="Randomize New Circuit & Board", command=self.reset_board)
        self.reset_button.pack(side=tk.LEFT, padx=5)

        self.path = []
        self.current_index = 0
        self.animation_id = None
        self.short_positions = []
        self.board = []

        self.generate_random_circuit()
        self.draw_board()

    def generate_random_circuit(self):
        # 1. Start with an empty board (all 0s)
        self.board = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        
        # 2. Generate a random winding copper trace path (1s) starting from (0,0)
        curr_r, curr_c = 0, 0
        self.board[curr_r][curr_c] = 1
        trace_path = [(curr_r, curr_c)]
        
        # Walk randomly across the grid to build a unique copper trace each time
        for _ in range(random.randint(8, 14)):
            neighbors = []
            for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]:
                nr, nc = curr_r + dr, curr_c + dc
                if 0 <= nr < self.rows and 0 <= nc < self.cols and self.board[nr][nc] == 0:
                    neighbors.append((nr, nc))
            
            if not neighbors:
                break
            
            curr_r, curr_c = random.choice(neighbors)
            self.board[curr_r][curr_c] = 1
            trace_path.append((curr_r, curr_c))

        # 3. Randomly place 1 or 2 short circuits (2s) onto the generated copper trace
        if len(trace_path) >= 4:
            fault_spots = random.sample(trace_path[2:], min(2, len(trace_path)-2))
            for fr, fc in fault_spots:
                self.board[fr][fc] = 2

    def color_for_cell(self, value):
        if value == 0:
            return "#1e1e1e"  # Empty space
        elif value == 1:
            return "#28a745"  # Clean copper trace
        elif value == 2:
            return "#dc3545"  # Short circuit
        return "white"

    def draw_board(self):
        self.canvas.delete("all")
        for r in range(self.rows):
            for c in range(self.cols):
                x1 = c * self.cell_size
                y1 = r * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size

                color = self.color_for_cell(self.board[r][c])
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="#333", width=2)
                
                self.canvas.create_text(x1 + self.cell_size/2, y1 + self.cell_size/2, 
                                        text=f"({r},{c})", fill="#888" if self.board[r][c]==0 else "#fff", font=("Arial", 8, "bold"))

    def reset_board(self):
        if self.animation_id:
            self.root.after_cancel(self.animation_id)
            self.animation_id = None
        
        self.current_index = 0
        self.path = []
        self.short_positions = []
        self.generate_random_circuit()
        self.status_var.set("New random circuit layout generated!")
        self.draw_board()

    def run_simulation(self):
        if self.animation_id:
            self.root.after_cancel(self.animation_id)
            self.animation_id = None

        result = find_short_circuit(self.board, start=(0, 0))
        self.path = result["path"]
        self.short_positions = result["positions"]
        self.current_index = 0

        if not self.path:
            self.status_var.set("Error: No valid trace path found from (0,0). Try resetting.")
            return

        self.status_var.set("Traversing randomized PCB grid via LIFO Stack...")
        self.animate_path(result["short_detected"])

    def animate_path(self, short_detected):
        if self.current_index < len(self.path):
            row, col = self.path[self.current_index]
            self.highlight_cell(row, col)
            self.current_index += 1
            self.animation_id = self.root.after(300, lambda: self.animate_path(short_detected))
        else:
            self.animation_id = None
            if short_detected:
                self.status_var.set(f"[!] Audit Complete. Short circuits found at: {self.short_positions}")
                messagebox.showerror("Faults Isolated!", f"LIFO Stack fully traversed the random circuit and caught all short circuits at: {self.short_positions}!")
            else:
                self.status_var.set("Audit Complete: Entire trace grid is safe.")
                messagebox.showinfo("Passed", "Stack traversal complete. No faults found.")

    def highlight_cell(self, row, col):
        x1 = col * self.cell_size
        y1 = row * self.cell_size
        x2 = x1 + self.cell_size
        y2 = y1 + self.cell_size

        if self.board[row][col] == 2:
            self.canvas.create_rectangle(x1+4, y1+4, x2-4, y2-4, fill="purple", outline="white", width=3, tags="highlight")
        else:
            self.canvas.create_rectangle(x1+4, y1+4, x2-4, y2-4, fill="#007bff", outline="yellow", width=2, tags="highlight")

def main():
    root = tk.Tk()
    PCBVisualizer(root)
    root.mainloop()

if __name__ == "__main__":
    main()
