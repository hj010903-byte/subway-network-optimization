"""GA was proposed in slides 5 and 10, but operators are absent from the notebook.
Only coverage-based initial population selection is exposed here.
"""
from .fitness import calculate_fitness

def select_initial_population(population, graph, top_n=10):
    if top_n < 1 or not graph.nodes:
        raise ValueError('top_n and graph node count must be positive')
    return sorted(population, key=lambda routes: calculate_fitness(routes, graph, len(graph))[0], reverse=True)[:top_n]

