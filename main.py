# main.py
import tkinter as tk
from pathfinder.gui import App
from pathfinder.constants import WINDOW_BG_COLOR, WINDOW_TITLE

def main():
    """Initializes and runs the Pathfinding Visualizer application."""
    root = tk.Tk()
    root.title(WINDOW_TITLE)
    root.configure(bg=WINDOW_BG_COLOR)
    
    # Prevents the window from being resizable
    root.resizable(False, False)
    
    app = App(root)
    root.mainloop()

if __name__ == "__main__":
    main()
