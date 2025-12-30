import networkx as nx
import numpy as np
from typing import TypeVar, NewType, List, Optional, Callable, Union
from collections.abc import Mapping
import heapq
from .constants import UP, DOWN, LEFT, RIGHT

T = TypeVar("T")
N = TypeVar("N")
Coordinate = NewType("Coordinate", tuple[int])
NumpySlice = NewType("NumpySlice", Union[slice, object])

# NOTE!!! NO NEGATIVE VALUES
class Grid:
    """
        Convention for mazes:
            0: empty space
            1: wall
            *_: define in set_mapping()        
    """
    
    def __init__(self, grid_data: list[Union[list[T], np.ndarray]], *, mapping: Mapping[T, N] = None) -> None:
        self.grid = np.array(grid_data)
        self.shape = self.grid.shape
        
        if mapping is not None: # user predefined mapping, mainly for printing
            self._mapping = mapping
            
        else: # unordered string -> int mapping
            self._mapping = {element: i for i, element in enumerate(set(np.ravel(self.grid)))}
        
        keys, inv = np.unique(self.grid, return_inverse=True)
        vals = np.array([self._mapping[str(k)] for k in keys])
        self.grid = vals[inv].reshape(self.grid.shape)
        
        self._mapping = {v: k for k, v in self._mapping.items()} 
    
    @property    
    def visual(self) -> str:
        lookup = np.array([self._mapping[i] for i in range(max(self._mapping) + 1)])
        return "\n".join(map("".join, lookup[self.grid]))
    
    def set_mapping(self, new_mapping: Mapping[N, T]) -> None:
        # note the type hint, grid is translated after initialisation so mapping needs to be reversed
        self._mapping = new_mapping
        
    def __str__(self) -> str: # doesn't work for numbers > 10
        return "\n".join(map("".join, self.grid.astype(str)))

    def __repr__(self):
        return str(self)
        
    def __getitem__(self, key: NumpySlice) -> T:
        return self.grid[key]
    
    def __setitem__(self, key: NumpySlice, value: T) -> None:
        self.grid[key] = value
        
    def bounds(self, coord: Coordinate) -> bool:
        return 0 <= coord[0] < self.shape[0] and 0 <= coord[1] < self.shape[1]

    def astar(self, start: Coordinate, end: Coordinate) -> list[Coordinate]: # returns shortest path
        def reconstruct_path(came_from: dict[Coordinate, Coordinate], current: Coordinate) -> list[Coordinate]:
            path = [current]
            
            while current in came_from.keys():
                current = came_from[current]
                path.append(current)
            
            return path[::-1]
        
        # manhattan heuristic over euclidean for only cardinal movements
        heuristic: Callable[Coordinate, float] = lambda yx: np.sum(np.abs(np.array(yx) - end))
        
        open_set = [(heuristic(start), tuple(start))]
        os_set = {tuple(start)}
        came_from = {}
        
        g = np.full(self.shape, fill_value=np.inf, dtype=float)
        f = np.full(self.shape, fill_value=np.inf, dtype=float)
        
        g[*start] = 0
        f[*start] = heuristic(start)
        
        while open_set:
            _, current = heapq.heappop(open_set)
            os_set.remove(current)
        
            if np.all(current == end):
                return reconstruct_path(came_from, current)
            
            for direction in [UP, DOWN, LEFT, RIGHT]:
                check = np.array(current) + direction
                
                if not self.bounds(check) or self.grid[*check] == -1:
                    continue
                
                if (tentative := g[*current] + 1) < g[*check]:
                    came_from[tuple(check)] = current
                    g[*check] = tentative
                    f[*check] = tentative + heuristic(check)
                    
                    if not tuple(check) in os_set:
                        heapq.heappush(open_set, (f[*check], tuple(check)))
                        os_set.add(tuple(check))
        
        return []
    
    def __iter__(self) -> None:
        return self
    
    def __next__(self) -> None:
        return self

class Graph(nx.Graph):
    def __init__(self, graph_data: List[T]) -> None:
        super().__init__(graph_data)
        
    # TODO/see networkx docs
