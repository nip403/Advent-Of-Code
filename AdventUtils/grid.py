import networkx as nx
import numpy as np
from typing import TypeVar, NewType, List, Optional, Callable, Union
from collections.abc import Mapping
import heapq
from .constants import UP, DOWN, LEFT, RIGHT

T = TypeVar("T")
Coordinate = NewType("Coordinate", tuple[int])
NumpySlice = NewType("NumpySlice", Union[slice, object])

# Note - it's not always the case that storing everything as a map is the best idea: if there are different objects with different conditions over a sparse map, it may well be better to just keep lists for each object in an iterator parent 
class Grid:
    """
        Convention for mazes:
            0: empty space
            -1: wall
            *_: define in set_mapping()        
    """
    _empty_space = 0
    _wall_space = -1
    
    def __init__(self, grid_data: list[Union[list[T], np.ndarray]], *, dtype: T) -> None:
        self.grid = np.array(grid_data, dtype=dtype)
        self.dtype = dtype
        self._mapping = dict()
        self.shape = self.grid.shape
        
    def set_mapping(self, mapping: Optional[Union[Mapping[str, int], Mapping[int, str], Mapping[str, str]]] = None) -> None:
        if mapping is not None: # user predefined mapping, mainly for printing
            self._mapping = mapping
            
        else: # assumes we want an unordered string -> int mapping
            self._mapping = {element: i for i, element in enumerate(set(np.ravel(self.grid)))}
    
    def mapped(self) -> np.ndarray[Union[str | int]]:
        return np.vectorize(self._mapping.get)(self.grid)
    
    def __str__(self) -> str: # NOTE: provide an int-to-string mapping if you have ints > 10
        return "\n".join(
            "".join([
                str(self._mapping.get(item, item)) 
            for item in row
            ]) 
        for row in self.grid
        )
        
    def __repr__(self):
        return str(self)
        
    def __getitem__(self, key: NumpySlice) -> T:
        return self.grid[key]
    
    def __setitem__(self, key: NumpySlice, value: T) -> None:
        assert type(value) == self.dtype, f"Shape or dtype set is inconsistent. Set dtype: {type(value)}, Ndarray dtype: {self.dtype}"
        
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
