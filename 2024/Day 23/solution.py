from pathlib import Path
import networkx as nx
import itertools as it
import numpy as np
import re

with open(Path(__file__).parent / "input_data.txt", "r") as f:
    data = f.read()

def build_graph(connections: list[str]) -> list[str]: 
    # create a node-int mapping for sorting
    computers = {c: i for i, c in enumerate(set(np.ravel(connections)))}

    graph = nx.Graph()
    graph.add_edges_from(connections)
    
    return graph, computers
    
def main(data: str) -> tuple[int]:
    connections = np.reshape(re.split("-|\n", data), (-1, 2))
    graph, computers = build_graph(connections)
    
    # Part 1    
    t_cycles = 0
    seen = set()
    max_clique = []
    
    for clique in nx.find_cliques(graph):
        if len(clique) > len(max_clique):
            max_clique = clique
            
        if len(clique) >= 3:
            for i in it.combinations(clique, 3):                
                seen.add(tuple(sorted(i, key=lambda x: computers[x])))
                
    t_cycles = sum(any(node.startswith("t") for node in triangle) for triangle in seen)

    # Part 2 - find maximum clique
    password = ",".join(sorted(max_clique, key=lambda x: ord(x[0]) * 26 + ord(x[1]))) # encode 2d -> 1d ranking

    return t_cycles, password

if __name__ == "__main__":
    print(main(data))