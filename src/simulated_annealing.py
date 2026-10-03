"""Cell 30 algorithm preserved; score_func receives (routes, od, nodes, graph)."""
import copy
import random
import numpy as np

def generate_neighbor_soft(individual, graph, num_swaps=2):
    neighbor = copy.deepcopy(individual)
    candidates = [i for i, (line_num, path) in enumerate(neighbor) if line_num != 100 and len(path) > 3]
    if not candidates:
        return neighbor
    idx = random.choice(candidates)
    line_num, path = neighbor[idx]
    for _ in range(num_swaps):
        i = random.randint(1, len(path) - 3)
        if graph.has_edge(path[i-1], path[i+1]) and graph.has_edge(path[i], path[i+2]):
            path[i], path[i+1] = path[i+1], path[i]
    neighbor[idx] = (line_num, path)
    return neighbor

def simulated_annealing(individual, score_func, od_dict, node_dict, graph, T=1.0, alpha=0.995, iterations=500):
    current = copy.deepcopy(individual)
    best = copy.deepcopy(individual)
    best_score = score_func(best, od_dict, node_dict, graph)
    current_score = best_score
    for _ in range(iterations):
        neighbor = generate_neighbor_soft(current, graph)
        neighbor_score = score_func(neighbor, od_dict, node_dict, graph)
        if neighbor_score > current_score:
            current = neighbor
            current_score = neighbor_score
            if neighbor_score > best_score:
                best = neighbor
                best_score = neighbor_score
        else:
            prob = np.exp((neighbor_score - current_score) / T)
            if random.random() < prob:
                current = neighbor
                current_score = neighbor_score
        T *= alpha
    return best, best_score
