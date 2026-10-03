"""Original cell 22 checks ALL node triples, not only graph triangles.
This may remove an edge even when the alternate two edges are absent.
"""
from itertools import combinations
import numpy as np
def is_obtuse(p1, p2, p3):
    a = np.linalg.norm(np.array(p1) - np.array(p2))
    b = np.linalg.norm(np.array(p2) - np.array(p3))
    c = np.linalg.norm(np.array(p3) - np.array(p1))
    sides = sorted([a, b, c])
    return sides[0]**2 + sides[1]**2 < sides[2]**2

def remove_obtuse_longest_edges(graph):
    refined = graph.copy()
    removal = set()
    for triangle in combinations(list(refined.nodes), 3):
        points = [refined.nodes[n]['pos'] for n in triangle]
        if is_obtuse(*points):
            distances = {
                (triangle[0], triangle[1]): np.linalg.norm(np.array(points[0]) - np.array(points[1])),
                (triangle[1], triangle[2]): np.linalg.norm(np.array(points[1]) - np.array(points[2])),
                (triangle[2], triangle[0]): np.linalg.norm(np.array(points[2]) - np.array(points[0]))
            }
            removal.add(tuple(sorted(max(distances, key=distances.get))))
    refined.remove_edges_from(removal)
    return refined
