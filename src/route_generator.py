"""Original A* variant and candidate diversification, not a global optimizer.
The unscaled Euclidean heuristic is preserved for historical fidelity.
It can overestimate randomized costs, so shortest-path optimality is not assured.
"""
import random
import numpy as np
from heapq import heappush, heappop
def heuristic(a, b):
    return np.linalg.norm(np.array(a) - np.array(b))

def random_a_star(graph, start, goal, used_edges):
    open_set = []
    heappush(open_set, (0, start))
    came_from = {}
    g_score = {node: float('inf') for node in graph.nodes}
    g_score[start] = 0
    f_score = {node: float('inf') for node in graph.nodes}
    f_score[start] = heuristic(graph.nodes[start]['pos'], graph.nodes[goal]['pos'])
    while open_set:
        _, current = heappop(open_set)
        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            return path[::-1]
        neighbors = list(graph.neighbors(current))
        random.shuffle(neighbors)
        for neighbor in neighbors:
            edge = tuple(sorted((current, neighbor)))
            if edge in used_edges:
                continue
            tentative_g = g_score[current] + graph[current][neighbor]['weight']
            if tentative_g < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score[neighbor] = tentative_g + heuristic(graph.nodes[neighbor]['pos'], graph.nodes[goal]['pos'])
                heappush(open_set, (f_score[neighbor], neighbor))
    return None

def randomize_weights(graph, seed=None):
    rng = random.Random(seed)
    candidate = graph.copy()
    for u, v in candidate.edges():
        distance = np.linalg.norm(np.array(candidate.nodes[u]['pos']) - np.array(candidate.nodes[v]['pos']))
        candidate[u][v]['weight'] = distance * rng.uniform(0.1, 1.9)
    return candidate

def generate_routes(graph, terminal_pairs, fixed_path=None):
    """Cell 26 pattern. Failed paths are omitted, so nine lines are not guaranteed."""
    fixed_path = list(fixed_path or [])
    routes = [(100, fixed_path)] if fixed_path else []
    used = {tuple(sorted((u, v))) for u, v in zip(fixed_path[:-1], fixed_path[1:])}
    for i, (start, goal) in enumerate(terminal_pairs):
        if start not in graph or goal not in graph:
            raise ValueError('Terminal identifier is absent from graph')
        path = random_a_star(graph, start, goal, used)
        if path:
            used.update(tuple(sorted((u, v))) for u, v in zip(path[:-1], path[1:]))
            routes.append((i, path))
    return routes
