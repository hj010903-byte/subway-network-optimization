"""KDTree construction from original cell 6, with small-input validation added."""
import networkx as nx
import numpy as np
import pandas as pd
import heapq
from scipy.spatial import KDTree

def build_knn_graph(stations, k=5):
    if k < 1:
        raise ValueError('k must be positive')
    coords = list(zip(stations['경도'], stations['위도']))
    graph = nx.Graph()
    for idx, pos in enumerate(coords):
        graph.add_node(idx, pos=pos, station_name=stations.iloc[idx]['역명'])
    if len(coords) < 2:
        return graph
    tree = KDTree(coords)
    for idx, coord in enumerate(coords):
        _, indices = tree.query(coord, k=min(k + 1, len(coords)))
        for neighbor in np.atleast_1d(indices):
            neighbor = int(neighbor)
            if neighbor != idx:
                distance = np.linalg.norm(np.array(coord) - np.array(coords[neighbor]))
                graph.add_edge(idx, neighbor, weight=float(distance))
    return graph

def load_edge_graph(path):
    """Original cell 26 uses station names as identifiers in the edge table."""
    frame = pd.read_excel(path)
    required = {'from', 'to', 'from_lon', 'from_lat', 'to_lon', 'to_lat', 'distance'}
    if not required.issubset(frame.columns):
        raise ValueError(f'Missing columns: {sorted(required - set(frame.columns))}')
    graph = nx.Graph()
    for _, row in frame.iterrows():
        graph.add_node(row['from'], pos=(row['from_lon'], row['from_lat']))
        graph.add_node(row['to'], pos=(row['to_lon'], row['to_lat']))
        graph.add_edge(row['from'], row['to'], weight=row['distance'])
    return graph


def prim_mst(graph, start_node):
    visited = set()
    mst = nx.Graph()
    pos = nx.get_node_attributes(graph, 'pos')

    for node in graph.nodes:
        mst.add_node(node, pos=pos[node])

    visited.add(start_node)
    edges = []

    for neighbor in graph.neighbors(start_node):
        weight = graph[start_node][neighbor]['weight']
        heapq.heappush(edges, (weight, start_node, neighbor))

    while edges and len(visited) < len(graph.nodes):
        weight, u, v = heapq.heappop(edges)
        if v not in visited:
            visited.add(v)
            mst.add_edge(u, v, weight=weight)
            for neighbor in graph.neighbors(v):
                if neighbor not in visited:
                    new_weight = graph[v][neighbor]['weight']
                    heapq.heappush(edges, (new_weight, v, neighbor))

    return mst
