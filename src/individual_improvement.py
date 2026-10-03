"""Cell 32 preserved experiments: can mutate graph and introduce unvalidated edges."""
import random
import numpy as np
from .fitness import angle_between_nodes, calculate_combined_fitness

def improve_individual_by_angle_with_batch_insertion(individual, graph, min_angle=60, batch_size=4):
    improved = [ (lnum, path[:]) for lnum, path in individual ]
    candidates = []

    # 각도 min_angle 미만인 지점 수집
    for line_idx, (lnum, path) in enumerate(improved):
        if lnum == 100 or len(path) < 3:
            continue
        for i in range(1, len(path) - 1):
            u, v, w = path[i - 1], path[i], path[i + 1]
            angle = angle_between_nodes(graph.nodes[u]['pos'], graph.nodes[v]['pos'], graph.nodes[w]['pos'])
            if angle < min_angle:
                candidates.append((line_idx, i, v))

    if not candidates:
        return improved

    selected = random.sample(candidates, min(batch_size, len(candidates)))
    removed_nodes = []

    for line_idx, del_idx, bad_node in selected:
        lnum, path = improved[line_idx]
        if del_idx < len(path):
            new_path = path[:del_idx] + path[del_idx+1:]
            improved[line_idx] = (lnum, new_path)
            removed_nodes.append(bad_node)

    for bad_node in removed_nodes:
        best_dist = float('inf')
        best_insert = None

        for i, (lnum2, path2) in enumerate(improved):
            if len(path2) < 2:
                continue
            for j in range(len(path2) - 1):
                a, b = path2[j], path2[j + 1]
                pos_a = graph.nodes[a]['pos']
                pos_b = graph.nodes[b]['pos']
                pos_v = graph.nodes[bad_node]['pos']
                dist = np.linalg.norm(np.array(pos_v) - (np.array(pos_a) + np.array(pos_b)) / 2)
                if dist < best_dist:
                    best_dist = dist
                    best_insert = (i, j + 1)

        if best_insert:
            i, insert_pos = best_insert
            lnum2, path2 = improved[i]
            if bad_node not in path2:
                a = path2[insert_pos - 1]
                b = path2[insert_pos]
                if not graph.has_edge(a, bad_node):
                    dist1 = np.linalg.norm(np.array(graph.nodes[a]['pos']) - np.array(graph.nodes[bad_node]['pos']))
                    graph.add_edge(a, bad_node, weight=dist1)
                if not graph.has_edge(bad_node, b):
                    dist2 = np.linalg.norm(np.array(graph.nodes[bad_node]['pos']) - np.array(graph.nodes[b]['pos']))
                    graph.add_edge(bad_node, b, weight=dist2)

                new_path2 = path2[:insert_pos] + [bad_node] + path2[insert_pos:]
                improved[i] = (lnum2, new_path2)

    return improved

def improve_by_batch_safe_granular(individual, graph, od_dict, node_dict, iterations=10, batch_size=4, min_angle=60):
    current = [ (lnum, path[:]) for lnum, path in individual ]
    current_score = calculate_combined_fitness(current, od_dict, node_dict, graph)

    for _ in range(iterations):
        # 꺾인 점 후보 수집
        candidates = []
        for line_idx, (lnum, path) in enumerate(current):
            if lnum == 100 or len(path) < 3:
                continue
            for i in range(1, len(path) - 1):
                u, v, w = path[i - 1], path[i], path[i + 1]
                angle = angle_between_nodes(graph.nodes[u]['pos'], graph.nodes[v]['pos'], graph.nodes[w]['pos'])
                if angle < min_angle:
                    candidates.append((line_idx, i, v))

        if not candidates:
            break  # 개선할 점이 없음

        selected = random.sample(candidates, min(batch_size, len(candidates)))

        for line_idx, del_idx, bad_node in selected:
            # 현재 상태를 복사
            trial = [ (lnum, path[:]) for lnum, path in current ]
            lnum, path = trial[line_idx]

            # 노드 제거
            if del_idx >= len(path): continue
            path = path[:del_idx] + path[del_idx+1:]
            trial[line_idx] = (lnum, path)

            # 삽입 위치 탐색
            best_dist = float('inf')
            best_insert = None
            for i, (lnum2, path2) in enumerate(trial):
                if len(path2) < 2 or bad_node in path2: continue
                for j in range(len(path2) - 1):
                    a, b = path2[j], path2[j + 1]
                    pos_a = graph.nodes[a]['pos']
                    pos_b = graph.nodes[b]['pos']
                    pos_v = graph.nodes[bad_node]['pos']
                    dist = np.linalg.norm(np.array(pos_v) - (np.array(pos_a) + np.array(pos_b)) / 2)
                    if dist < best_dist:
                        best_dist = dist
                        best_insert = (i, j + 1)

            # 삽입 시도
            if best_insert:
                i, insert_pos = best_insert
                lnum2, path2 = trial[i]
                a = path2[insert_pos - 1]
                b = path2[insert_pos]
                if not graph.has_edge(a, bad_node):
                    dist1 = np.linalg.norm(np.array(graph.nodes[a]['pos']) - np.array(graph.nodes[bad_node]['pos']))
                    graph.add_edge(a, bad_node, weight=dist1)
                if not graph.has_edge(bad_node, b):
                    dist2 = np.linalg.norm(np.array(graph.nodes[bad_node]['pos']) - np.array(graph.nodes[b]['pos']))
                    graph.add_edge(bad_node, b, weight=dist2)
                new_path2 = path2[:insert_pos] + [bad_node] + path2[insert_pos:]
                trial[i] = (lnum2, new_path2)

            # 개선 여부 판단
            trial_score = calculate_combined_fitness(trial, od_dict, node_dict, graph)
            if trial_score >= current_score:
                current = trial
                current_score = trial_score


    return current
