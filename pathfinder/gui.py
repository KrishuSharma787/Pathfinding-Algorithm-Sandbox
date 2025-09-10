# pathfinder/gui.py
import tkinter as tk
from tkinter import ttk
import time
import random

# Import from other modules in the package
from .constants import *
from .grid import Grid
from . import algorithms

class App:
    def __init__(self, root):
        self.root = root
        self.grid = Grid()
        self.mode = "wall"
        self.algorithm = tk.StringVar(value="A*")
        self.running = False

        # Map algorithm names to their functions
        self.algorithms = {
            "A*": algorithms.a_star,
            "Dijkstra": algorithms.dijkstra,
            "BFS": algorithms.bfs,
            "DFS": algorithms.dfs,
        }

        self._setup_styles()
        self._create_widgets()
        self._bind_shortcuts()
        self.draw_grid()
    
    # ... (All the methods from your App class go here) ...
    # (on_click, on_drag, draw_grid, run, clear_walls, reset, generate_maze, etc.)
    # I will paste the full class content below for completeness.
