# pathfinder/algorithms.py
from queue import Queue, PriorityQueue
from .grid import manhattan_distance

def reconstruct_path(parent, start, end):
    """Reconstructs the path from end to start using the parent map."""
    path = set()
    cur = end
    while cur != start:
        path.add(cur)
        cur = parent[cur]
    path.add(start)
    return path

def bfs(grid):
    """Breadth-First Search algorithm."""
    start, end = grid.start, grid.end
    q = Queue()
    q.put(start)
    visited = {start}
    parent = {}

    while not q.empty():
        cur = q.get()
        if cur == end:
            return visited, reconstruct_path(parent, start, end)
        for nb in grid.neighbors(*cur):
            if nb not in visited:
                visited.add(nb)
                parent[nb] = cur
                q.put(nb)
    return visited, set() # Path not found

def dfs(grid):
    """Depth-First Search algorithm."""
    start, end = grid.start, grid.end
    stack = [start]
    visited = {start}
    parent = {}

    while stack:
        cur = stack.pop()
        if cur == end:
            return visited, reconstruct_path(parent, start, end)
        for nb in grid.neighbors(*cur):
            if nb not in visited:
                visited.add(nb)
                parent[nb] = cur
                stack.append(nb)
    return visited, set() # Path not found

def dijkstra(grid):
    """Dijkstra's algorithm."""
    start, end = grid.start, grid.end
    pq = PriorityQueue()
    pq.put((0, start))
    dist = {start: 0}
    parent = {}
    visited = set()

    while not pq.empty():
        d, cur = pq.get()
        if cur in visited:
            continue
        visited.add(cur)
        if cur == end:
            return visited, reconstruct_path(parent, start, end)
        for nb in grid.neighbors(*cur):
            nd = d + 1
            if nd < dist.get(nb, float('inf')):
                dist[nb] = nd
                parent[nb] = cur
                pq.put((nd, nb))
    return visited, set() # Path not found

def a_star(grid):
    """A* search algorithm."""
    start, end = grid.start, grid.end
    pq = PriorityQueue()
    g_score = {start: 0}
    f_score = {start: manhattan_distance(start, end)}
    pq.put((f_score[start], start))
    parent = {}
    visited = set()

    while not pq.empty():
        _, cur = pq.get()
        if cur in visited:
            continue
        visited.add(cur)
        if cur == end:
            return visited, reconstruct_path(parent, start, end)
        for nb in grid.neighbors(*cur):
            tentative_g = g_score[cur] + 1
            if tentative_g < g_score.get(nb, float('inf')):
                parent[nb] = cur
                g_score[nb] = tentative_g
                f_score[nb] = tentative_g + manhattan_distance(nb, end)
                pq.put((f_score[nb], nb))
    return visited, set() # Path not found
