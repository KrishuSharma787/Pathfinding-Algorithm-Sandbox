# Pathfinding-Algorithm-Sandbox

<p align="center">
  <img alt="Python Version" src="https://img.shields.io/badge/python-3.9%2B-blue.svg">
  <img alt="License" src="https://img.shields.io/badge/license-MIT-green.svg">
  <img alt="Platform" src="https://img.shields.io/badge/platform-cross--platform-lightgrey.svg">
</p>

<p align="center">
  An interactive desktop application for visualizing fundamental graph traversal and pathfinding algorithms, built with Python and Tkinter.
</p>

---

<p align="center">
  
  <br>

</p>

---

## Table of Contents

- [About The Project](#about-the-project)
- [Key Features](#key-features)
- [Getting Started](#getting-started)
- [How to Operate](#how-to-operate)
- [License](#license)
- [Contact](#contact)

---

## About The Project

This project provides an interactive platform to understand and compare the behavior of classic pathfinding algorithms. By allowing users to draw obstacles, place start and end points, and generate complex mazes, it offers a hands-on learning experience for these core computer science concepts.

The visualizer is designed not only as an educational tool but also as a demonstration of clean software architecture, including the separation of UI, data model, and algorithmic logic.

### Built With

This application is built exclusively with standard Python libraries, ensuring high portability and no external dependencies.

* **[Python 3](https://www.python.org/)**
* **[Tkinter](https://docs.python.org/3/library/tkinter.html)** (for the graphical user interface)

---

## Key Features

#### ✅ Core Algorithms Implemented
* **A\* Search:** Utilizes the Manhattan distance heuristic to find the shortest path in an optimal manner.
* **Dijkstra's Algorithm:** Guarantees the shortest path from the start to all other nodes.
* **Breadth-First Search (BFS):** An unweighted algorithm ideal for finding the shortest path in terms of the number of cells.
* **Depth-First Search (DFS):** Explores as far as possible down each branch before backtracking, finding a path but not necessarily the shortest one.

#### ✅ Interactive User Interface
* **Dynamic Grid:** A fully interactive grid where users can draw walls, and set custom start and end points.
* **Real-time Drawing:** Click or drag the mouse to create complex obstacles and patterns on the grid.
* **Maze Generation:** Implements a randomized Depth-First Search algorithm to generate intricate mazes with a single click.
* **Responsive Controls:** A clean and intuitive control panel for algorithm selection and grid manipulation.

#### ✅ User Experience
* **Status Bar:** Provides instant feedback on the selected algorithm, number of cells visited, path length, and execution time in milliseconds.
* **Keyboard Shortcuts:** Optimized for power users with intuitive keybindings for all major functions.
* **Modular & Clean UI:** A modern interface built using themed Tkinter widgets for a professional look and feel.

---

## Getting Started

To get a local copy up and running, follow these simple steps.

### Prerequisites

-   Python 3.6 or newer.
-   Tkinter is required, which is included in most standard Python installations. If it's missing, you can install it using your system's package manager (e.g., `sudo apt-get install python3-tk` on Debian/Ubuntu).

### Installation & Launch

1.  **Clone the repository:**
    ```sh
    git clone [https://github.com/your-username/pathfinding-visualizer.git](https://github.com/your-username/pathfinding-visualizer.git)
    cd pathfinding-visualizer
    ```

2.  **Run the application:**
    ```sh
    python main.py
    ```

---

## How to Operate

The application is designed for ease of use.

| Control                 | Action                                                                   |
| ----------------------- | ------------------------------------------------------------------------ |
| **Algorithm Selection** | Use the dropdown menu to select the desired pathfinding algorithm.       |
| **Drawing Mode** | Select "Wall", "Start", or "End" radio buttons to define your cursor mode. |
| **Drawing Walls** | In "Wall" mode, click a cell to place a wall, or click and drag to draw. |
| **Placing Nodes** | In "Start" or "End" mode, click a cell to move the respective node.      |
| **Run** | Click the **Run** button or press `R` to start the visualization.          |
| **Generate Maze** | Click the **Generate Maze** button to create a new random maze.            |
| **Clear Walls** | Click the **Clear Walls** button or press `C` to remove all walls.         |
| **Reset Grid** | Click the **Reset** button or press `Esc` to restore the grid to default.  |

---

## License

Distributed under the MIT License. See `LICENSE` file for more information.

---

## Contact

Krishu Sharma - krishu.sharma787@gmail.com


---
