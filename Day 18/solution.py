from pathlib import Path
import numpy as np
from collections import deque
from typing import NewType, Callable
import heapq
import copy
import re

Coordinate = NewType("Coordinate", tuple[int])

UP = np.array([-1, 0], dtype=int)
DOWN = np.array([1, 0], dtype=int)
LEFT = np.array([0, -1], dtype=int)
RIGHT = np.array([0, 1], dtype=int)

with open(Path(__file__).parent / "input_data.txt", "r") as f:
    data = f.read()

class MemorySpace:
    def __init__(self, corrupt_order: np.ndarray, shape: np.ndarray = (71, 71)) -> None:
        self.idx = deque(corrupt_order)
        self.space = np.zeros(shape, dtype=int)
        self.shape = shape
    
    def __iter__(self) -> None:
        return self
    
    def __next__(self) -> None:
        self.space[*self.idx.popleft()] = -1
        
    def __str__(self) -> str:
        lookup = np.array([" ", "O", "."], dtype="str")
        return "\n".join("".join(row) for row in lookup[self.space])
        
    def bounds(self, coord: Coordinate) -> bool:
        return 0 <= coord[0] < self.shape[0] and 0 <= coord[1] < self.shape[1]

    def astar(self, start: Coordinate, end: Coordinate) -> list[Coordinate]:
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
            f0, current = heapq.heappop(open_set)
            os_set.remove(current)
        
            if np.all(current == end):
                return reconstruct_path(came_from, current)
            
            for direction in [UP, DOWN, LEFT, RIGHT]:
                check = np.array(current) + direction
                
                if not self.bounds(check) or self.space[*check] == -1:
                    continue
                
                if (tentative:= g[*current] + 1) < g[*check]:
                    came_from[tuple(check)] = current
                    g[*check] = tentative
                    f[*check] = tentative + heuristic(check)
                    
                    if not tuple(check) in os_set:
                        heapq.heappush(open_set, (f[*check], tuple(check)))
                        os_set.add(tuple(check))
        
        return []
    
    def find_block(self, start: Coordinate, end: Coordinate) -> Coordinate:
        path = self.astar(start, end)
        
        while True: 
            candidate = self.idx[0]
            next(self)
            
            if tuple(candidate) in path:
                path = self.astar(start, end)
                
                if not path:
                    return candidate[::-1]
    
    def print_solved(self, start: Coordinate, end: Coordinate) -> None:
        results = tuple(zip(*self.astar(start, end)))
        self.space[results] = 1
        print(self)
        self.space[results] = 0

def main(data: str) -> tuple[int]:
    fall = np.reshape(re.split(r"\n|,", data), (-1, 2)).astype(int)
    start = np.zeros(2, dtype=int)
    end = np.array([70, 70], dtype=int)   
        
    space = MemorySpace(fall[:, ::-1]) # [[y x]]
    
    for _ in range(1024):
        next(space)
     
    snapshot = copy.deepcopy(space)
    #space.print_solved(start, end)

    return len(snapshot.astar(start, end)) - 1, ",".join(str(i) for i in space.find_block(start, end))

if __name__ == "__main__":
    print(main(data))