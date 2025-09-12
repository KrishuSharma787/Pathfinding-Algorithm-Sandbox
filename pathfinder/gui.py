# pathfinder/gui.py
import tkinter as tk
from tkinter import ttk, messagebox
import time
import random

from .constants import *
from .grid import Grid
from . import algorithms

class App:
    def __init__(self, root):
        self.root = root
        self.grid = Grid()
        self.mode = "wall"
        self.algorithm_name = tk.StringVar(value="A*")
        self.running = False
        self.last_drag_cell = None  # For smooth drawing

        self.algorithms = {
            "A*": algorithms.a_star,
            "Dijkstra": algorithms.dijkstra,
            "BFS": algorithms.bfs,
            "DFS": algorithms.dfs,
        }

        self._setup_styles()
        self._create_widgets()
        self._bind_shortcuts()

    def _setup_styles(self):
        style = ttk.Style(self.root)
        style.theme_use("clam")
        style.configure(".", font=(FONT_FAMILY, FONT_SIZE_NORMAL))
        style.configure("TButton", font=(FONT_FAMILY, FONT_SIZE_NORMAL, "bold"), padding=(BUTTON_PADX, BUTTON_PADY), relief="flat", background="#f0f0f0", foreground="#343a40")
        style.map("TButton", background=[("active", "#e0e0e0"), ("pressed", "#d0d0d0")], foreground=[("active", "#212529")])
        style.configure("TMenubutton", font=(FONT_FAMILY, FONT_SIZE_NORMAL, "bold"), padding=(BUTTON_PADX, BUTTON_PADY), relief="flat", background="#f0f0f0", foreground="#343a40")
        style.map("TMenubutton", background=[("active", "#e0e0e0"), ("pressed", "#d0d0d0")], foreground=[("active", "#212529")])
        style.configure("TLabel", background=self.root["bg"], foreground="#343a40")
        style.configure("TFrame", background=self.root["bg"])
        style.configure("TRadiobutton", background=self.root["bg"], font=(FONT_FAMILY, FONT_SIZE_NORMAL))
        style.configure("TLabelframe", background=self.root["bg"], foreground="#343a40", font=(FONT_FAMILY, FONT_SIZE_NORMAL, "bold"))
        style.configure("TLabelframe.Label", background=self.root["bg"], foreground="#343a40")

    def _create_widgets(self):
        main_frame = ttk.Frame(self.root, padding=(FRAME_PADX, FRAME_PADY))
        main_frame.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(main_frame, width=COLS * CELL, height=ROWS * CELL, bg=COLOR_EMPTY, bd=0, highlightthickness=0)
        
        # Create and store cell widgets for efficient updates
        self.cell_widgets = [[None for _ in range(COLS)] for _ in range(ROWS)]
        for r in range(ROWS):
            for c in range(COLS):
                x0, y0 = c * CELL, r * CELL
                x1, y1 = x0 + CELL, y0 + CELL
                rect_id = self.canvas.create_rectangle(x0, y0, x1, y1, fill=COLOR_EMPTY, outline=COLOR_BORDER)
                self.cell_widgets[r][c] = rect_id

        self.canvas.pack(pady=(0, 10))
        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", lambda e: setattr(self, 'last_drag_cell', None))

        toolbar = ttk.Frame(main_frame)
        toolbar.pack(fill="x", pady=(0, 10))
        
        ttk.Label(toolbar, text="Algorithm:").pack(side="left", padx=(0, 5))
        algo_options = list(self.algorithms.keys())
        ttk.OptionMenu(toolbar, self.algorithm_name, algo_options[0], *algo_options).pack(side="left", padx=(0, 15))

        ttk.Button(toolbar, text="Run", command=self.run).pack(side="left", padx=5)
        ttk.Button(toolbar, text="Clear Walls", command=self.clear_walls).pack(side="left", padx=5)
        ttk.Button(toolbar, text="Reset", command=self.reset).pack(side="left", padx=5)
        ttk.Button(toolbar, text="Generate Maze", command=self.generate_maze).pack(side="left", padx=5)

        mode_frame = ttk.LabelFrame(main_frame, text=" Drawing Mode ", padding=(5,5))
        mode_frame.pack(fill="x", pady=(0, 10))
        self.mode_var = tk.StringVar(value="wall")
        ttk.Radiobutton(mode_frame, text="Wall (W)", variable=self.mode_var, value="wall", command=lambda: self.set_mode("wall")).pack(side="left", padx=5)
        ttk.Radiobutton(mode_frame, text="Start (S)", variable=self.mode_var, value="start", command=lambda: self.set_mode("start")).pack(side="left", padx=5)
        ttk.Radiobutton(mode_frame, text="End (E)", variable=self.mode_var, value="end", command=lambda: self.set_mode("end")).pack(side="left", padx=5)

        self.status = ttk.Label(main_frame, text="Select an algorithm and draw some walls!", anchor="w", padding=(5,5))
        self.status.pack(fill="x")

        self.draw_grid() # Initial full draw

    def _bind_shortcuts(self):
        self.root.bind("w", lambda e: self.set_mode("wall"))
        self.root.bind("s", lambda e: self.set_mode("start"))
        self.root.bind("e", lambda e: self.set_mode("end"))
        self.root.bind("r", lambda e: self.run())
        self.root.bind("c", lambda e: self.clear_walls())
        self.root.bind("<Escape>", lambda e: self.reset())

    def set_mode(self, mode):
        self.mode = mode
        self.mode_var.set(mode)

    def _update_cell_color(self, r, c, visited=None, path=None):
        """Efficiently updates a single cell's color, including algorithm results."""
        rect_id = self.cell_widgets[r][c]
        color = COLOR_EMPTY
        
        if path and (r, c) in path: color = COLOR_PATH
        elif (r, c) == self.grid.start: color = COLOR_START
        elif (r, c) == self.grid.end: color = COLOR_END
        elif visited and (r, c) in visited: color = COLOR_VISITED
        elif (r, c) in self.grid.walls: color = COLOR_WALL
        
        self.canvas.itemconfig(rect_id, fill=color)

    def on_click(self, event):
        if self.running: return
        r, c = event.y // CELL, event.x // CELL
        if not self.grid.in_bounds(r, c): return
        
        old_start, old_end = self.grid.start, self.grid.end
        
        if self.mode == "wall":
            if (r, c) != self.grid.start and (r, c) != self.grid.end:
                if (r, c) in self.grid.walls: self.grid.walls.remove((r, c))
                else: self.grid.walls.add((r, c))
                self._update_cell_color(r, c)
        elif self.mode == "start":
            if (r,c) not in self.grid.walls and (r,c) != self.grid.end:
                self.grid.start = (r, c)
                self._update_cell_color(old_start[0], old_start[1])
                self._update_cell_color(r, c)
        elif self.mode == "end":
            if (r,c) not in self.grid.walls and (r,c) != self.grid.start:
                self.grid.end = (r, c)
                self._update_cell_color(old_end[0], old_end[1])
                self._update_cell_color(r, c)

    def on_drag(self, event):
        if self.running: return
        r, c = event.y // CELL, event.x // CELL
        
        if self.grid.in_bounds(r, c) and (r, c) != self.last_drag_cell:
            self.last_drag_cell = (r, c)
            if self.mode == "wall":
                if (r, c) != self.grid.start and (r, c) != self.grid.end:
                    if (r,c) not in self.grid.walls:
                        self.grid.walls.add((r, c))
                        self._update_cell_color(r, c)

    def draw_grid(self, visited=set(), path=set()):
        """Performs a full, but efficient, redraw of the grid."""
        for r in range(ROWS):
            for c in range(COLS):
                self._update_cell_color(r, c, visited, path)

    def run(self):
        if self.running: return
        self.running = True
        self.draw_grid() # Clear previous run results
        
        algo_func = self.algorithms.get(self.algorithm_name.get())
        if not algo_func:
            messagebox.showerror("Error", "Algorithm not found.")
            self.running = False
            return

        start_time = time.time()
        visited, path = algo_func(self.grid)
        end_time = time.time()
        runtime_ms = int((end_time - start_time) * 1000)
        
        # Check if the path is empty and show a pop-up
        if not path and self.grid.start != self.grid.end:
            messagebox.showinfo(
                "Path Not Found", 
                "No path could be found from the start to the end node."
            )
        
        self.draw_grid(visited, path)
        self.status.config(
            text=f"Algorithm: {self.algorithm_name.get()} | Visited: {len(visited)} | Path: {len(path)} | Time: {runtime_ms} ms"
        )
        self.running = False

    def clear_walls(self):
        if self.running: return
        self.grid.walls.clear()
        self.draw_grid()

    def reset(self):
        if self.running: return
        self.grid = Grid()
        self.draw_grid()
        self.status.config(text="Grid has been reset.")
        self.set_mode("wall")

    def generate_maze(self):
        if self.running: return
        self.reset()
        
        # 1. Start with a grid full of walls
        for r in range(ROWS):
            for c in range(COLS):
                self.grid.walls.add((r,c))

        # 2. Carve a perfect maze using randomized DFS (Recursive Backtracker)
        walls_to_remove = set()
        stack = [(0,0)]
        visited_maze = {(0,0)}

        while stack:
            r, c = stack[-1]
            neighbors = []
            for dr, dc in [(0, 2), (0, -2), (2, 0), (-2, 0)]:
                nr, nc = r + dr, c + dc
                if self.grid.in_bounds(nr, nc) and (nr, nc) not in visited_maze:
                    neighbors.append((nr, nc))
            
            if neighbors:
                nr, nc = random.choice(neighbors)
                wall_between = (r + (nr-r)//2, c + (nc-c)//2)
                walls_to_remove.add((nr,nc))
                walls_to_remove.add(wall_between)
                visited_maze.add((nr, nc))
                stack.append((nr, nc))
            else:
                stack.pop()

        self.grid.walls -= walls_to_remove

        # 3. Explicitly clear a 1-block radius around the end node.
        end_r, end_c = self.grid.end
        for dr in range(-1, 2):
            for dc in range(-1, 2):
                nr, nc = end_r + dr, end_c + dc
                if self.grid.in_bounds(nr, nc) and (nr, nc) in self.grid.walls:
                    self.grid.walls.remove((nr, nc))
        
        # 4. Final check to ensure the start point is not a wall
        if self.grid.start in self.grid.walls:
            self.grid.walls.remove(self.grid.start)

        self.draw_grid()
