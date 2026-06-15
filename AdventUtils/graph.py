import numpy as np
from typing import Any, TypeVar, Hashable, List, Set, Optional
#import networkx as nx

T = TypeVar("T")

class UnionFind: # i hate graph theory
    def __init__(self, nodes: List[T]) -> None:
        self.parent = {node: node for node in nodes}
        self.sets = len(nodes)
        
    def find(self, node: T) -> None:
        if self.parent[node] == node:
            return node
        
        self.parent[node] = self.find(self.parent[node])
        
        return self.parent[node]
    
    def union(self, x: T, y: T) -> None:
        x_root = self.find(x)
        y_root = self.find(y)
        
        if x_root != y_root:
            self.parent[x_root] = y_root
            self.sets -= 1
        
    # https://www.kaggle.com/code/stpeteishii/disjoint-set-union-union-find-algorithm

class Graph[T]: 
    def __init__(self) -> None:
        self.graph = {}
    
    def add_node(self, node: T) -> None: 
        assert isinstance(node, Hashable), "Unhashable type: {node}."
        
        if not node in self.graph:
            self.graph[node] = set()
        
    def add_nodes(self, nodes: List[T]) -> None:
        for n in nodes:
            self.add_node(n)
            
    def add_edge(self, u: T, v: T) -> bool: # False if edge is already in the graph
        for n in [u, v]:
            if not n in self.graph:
                self.add_node(n)

        if v in self.graph[u]:
            return False

        self.graph[u].add(v)
        self.graph[v].add(u)
        
        return True
    
    def get_neighbours(self, node: T) -> List[T]:
        return self.graph[node]
    
    def get_connected_components(self) -> set[List[T]]: # DFS
        visited = set()
        components = []
        
        for node in self.graph:
            if node not in visited:
                subgraph = set()
                stack = [node]
                
                while stack:
                    current = stack.pop()
                    
                    if current not in visited:
                        visited.add(current)
                        subgraph.add(current)
                        stack.extend(set(self.get_neighbours(current)) - visited)
                        
                components.append(subgraph)
        
        return components
    
    # very slow
    def get_paths(self, start: T, end: T, path: Optional[List[T]] = None) -> List[List[T]]:
        if path is None:
            path = []
            
        path = path + [start]
        
        if start == end:
            return [path]
        
        if start not in self.graph or not self.graph[start]:
            return []
        
        paths = []
        
        for neighbour in self.graph[start]:
            if neighbour not in path:
                new = self.get_paths(neighbour, end, path)
                
                for p in new:
                    paths.append(p)
                    
        return paths
    
    def count_paths(self, start: T, end: T, avoid: Optional[Set[T]]) -> int:
        memo = {}
        
        if avoid is None:
            avoid = set()
            
        def dfs(current: T, stack: List[T]) -> int:
            if current == end:
                return 1
            
            if current in avoid:
                return 0
            
            if current not in self.graph or not self.graph[current]:
                return 0
            
            if current in memo:
                return memo[current]
            
            stack.add(current)
            
            total = 0
            for n in self.graph.get(current):
                total += dfs(n, stack)
                
            stack.remove(current)
            memo[current] = total
            
            return total
        
        return dfs(start, set())
    
    def __str__(self) -> str:
        return f"{self.graph}"
    
    # todo if (ever) needed - pathfinding, edge removal, number of paths (backtracking DFS), subgraphs/complements, cycles/cliques/independence sets

class DirectedGraph[T](Graph): 
    def __init__(self) -> None:
        super().__init__()
        
    def add_edge(self, u: T, v: T, directed=True):
        for n in [u, v]:
            if not n in self.graph:
                self.add_node(n)

        if v in self.graph[u]:
            return False

        self.graph[u].add(v)
        
        if not directed:
            self.graph[v].add(u)
        
        return True
    
    