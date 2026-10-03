"""Original cells 26 and 32. Combined score is not a coverage percentage."""
import numpy as np

def calculate_fitness(line_paths, G, total_nodes):
    visited_nodes = set()
    for _, path in line_paths:
        visited_nodes.update(path)
    node_score = len(visited_nodes) / total_nodes * 100
    return node_score, total_nodes - len(visited_nodes)

def fitness_path_length_range(individual, min_length=20, max_length=50):
    penalty = 0
    for line_num, path in individual:
        if line_num == 100: continue
        if len(path) < min_length:
            penalty += (min_length - len(path))**2
        elif len(path) > max_length:
            penalty += (len(path) - max_length)**2
    return -penalty

def angle_between_nodes(pos_u, pos_v, pos_w):
    vec1 = np.array(pos_u) - np.array(pos_v)
    vec2 = np.array(pos_w) - np.array(pos_v)
    cosine = np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))
    cosine = np.clip(cosine, -1.0, 1.0)
    return np.degrees(np.arccos(cosine))

def smooth_angle_penalty(line_paths, graph):
    penalty = 0
    for _, path in line_paths:
        if len(path) < 4:
            continue

        # 단일 각도 기준 (급격한 꺾임 탐지)
        for i in range(1, len(path) - 1):
            u, v, w = path[i - 1], path[i], path[i + 1]
            angle = angle_between_nodes(graph.nodes[u]['pos'], graph.nodes[v]['pos'], graph.nodes[w]['pos'])
            if angle < 90:
                penalty += (90 - angle)

        # 연속 각도의 변화량 기준
        for i in range(1, len(path) - 2):
            u1, v1, w1 = path[i - 1], path[i], path[i + 1]
            u2, v2, w2 = path[i], path[i + 1], path[i + 2]

            angle1 = angle_between_nodes(graph.nodes[u1]['pos'], graph.nodes[v1]['pos'], graph.nodes[w1]['pos'])
            angle2 = angle_between_nodes(graph.nodes[u2]['pos'], graph.nodes[v2]['pos'], graph.nodes[w2]['pos'])

            penalty += (abs(angle1 - angle2))

    return -penalty

def is_individual_angle_valid(individual, graph, min_angle=35):
    for _, path in individual:
        if len(path) < 3:
            continue
        for i in range(1, len(path) - 1):
            u, v, w = path[i - 1], path[i], path[i + 1]
            angle = angle_between_nodes(graph.nodes[u]['pos'], graph.nodes[v]['pos'], graph.nodes[w]['pos'])
            if angle < min_angle:
                return False
    return True

def calculate_combined_fitness(line_paths, od_dict, node_dict,
                                graph, alpha=1.0, beta=2.5, gamma=0.1, delta=0.013):
    od_score = 0
    for _, path in line_paths:
        for i in range(len(path)):
            for j in range(i + 1, len(path)):
                pair = (path[i], path[j])
                rev_pair = (path[j], path[i])
                if pair in od_dict:
                    od_score += od_dict[pair]
                elif rev_pair in od_dict:
                    od_score += od_dict[rev_pair]

    node_score = sum(node_dict.get(n, 0) for _, path in line_paths for n in path)
    length_penalty = fitness_path_length_range(line_paths)
    angle_penalty_val = smooth_angle_penalty(line_paths, graph)

    return alpha * od_score + beta * node_score + gamma * length_penalty + delta * angle_penalty_val
