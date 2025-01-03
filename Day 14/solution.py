from pathlib import Path
import numpy as np
from scipy.spatial import KDTree

with open(Path(__file__).parent / "input_data.txt", "r") as f:
    data = f.read()
    
class System:
    def __init__(self, robots: np.ndarray, bounds: np.ndarray) -> None:
        self.robots = robots
        self.bounds = bounds
        self.elapsed = 0
        
    def __iter__(self) -> None:
        return self
    
    def __next__(self) -> None:
        self.robots[:, 0] = (self.robots[:, 0] + self.robots[:, 1]) % self.bounds
        self.elapsed += 1
        return self

    def __str__(self) -> str:
        out = f"\nAfter {self.elapsed} seconds:\n"
        grid = np.zeros((self.bounds[1], self.bounds[0]), dtype=int)

        for pos in self.robots[:, 0]:
            grid[pos[1], pos[0]] += 1

        for row in grid:
            out += "".join(str(cell) if cell > 0 else "." for cell in row) + "\n"

        return out
    
    def quadrant_factor(self) -> int:
        return \
            np.sum(
                (self.robots[:, 0, 0] < self.bounds[0] // 2) & 
                (self.robots[:, 0, 1] < self.bounds[1] // 2)
            ) *\
            np.sum(
                (self.robots[:, 0, 0] >= self.bounds[0] - (self.bounds[0] // 2)) & 
                (self.robots[:, 0, 1] < self.bounds[1] // 2)
            ) *\
            np.sum(
                (self.robots[:, 0, 0] < self.bounds[0] // 2) & 
                (self.robots[:, 0, 1] >= self.bounds[1] - (self.bounds[1] // 2))
            )  *\
            np.sum(
                (self.robots[:, 0, 0] >= self.bounds[0] - (self.bounds[0] // 2)) & 
                (self.robots[:, 0, 1] >= self.bounds[1] - (self.bounds[1] // 2))
            ) 
            
    def neighbours(self) -> int:
        tree = KDTree(self.robots[:, 0])
        neighbours = tree.query_ball_point(self.robots[:, 0], 1)
        return (sum(len(n) for n in neighbours) - len(neighbours)) // 2

def main(data: str) -> tuple[int]:
    robots = np.array([
        [
            [
                int(k) for k in j.split("=")[1].split(",")
            ] 
            for j in i.split()
        ] 
        for i in data.splitlines()
    ])

    # Part 1
    system = System(robots, np.array([101, 103]))
    
    for i in range(1, 101):
        next(system)
        
    qfactor = system.quadrant_factor()
    
    # Part 2    
    while True:
        if system.neighbours() > 256: # thanks to someone on subreddit for their solution
            print(system)
            break
        
        i += 1
        next(system)

    return qfactor, i

if __name__ == "__main__":
    print(main(data))