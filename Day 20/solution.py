from pathlib import Path
from typing import NewType
from collections import defaultdict, Counter
import numpy as np

Coordinate = NewType("Coordinate", tuple[int])

np.set_printoptions(threshold=np.inf, suppress=True, linewidth=np.inf)

UP = np.array([-1, 0], dtype=int)
DOWN = np.array([1, 0], dtype=int)
LEFT = np.array([0, -1], dtype=int)
RIGHT = np.array([0, 1], dtype=int)

with open(Path(__file__).parent / "input_data.txt", "r") as f:
    data = f.read()

class Track:
    def __init__(self, racetrack: str) -> None:
        self.map = np.array([list(row) for row in racetrack.splitlines()])
        
        self.start = np.ravel(np.where(self.map == "S"))
        self.end = np.ravel(np.where(self.map == "E"))
        
        self.map = np.vectorize(lambda x: 0 if x in "SE." else 1)(self.map).astype(int)
        
        self.build_track()
        
    def __str__(self) -> str:
        lookup = np.array(list(" #."), dtype="str")
        return "\n".join("".join(row) for row in lookup[self.map])

    def build_track(self) -> None:
        current = self.start.copy()
        self.track = [tuple(current)]
        self.exposed = defaultdict(set) # all indices of walls exposed to track
        
        prev = None
        
        while True:
            for direction in [UP, DOWN, LEFT, RIGHT]:
                new = tuple(current + direction)
                
                if self.map[new]: # for part 1, only consider walls that touch track
                    if 0 < new[0] < self.map.shape[0] - 1 and 0 < new[1] < self.map.shape[1] - 1: # dont care about outer walls, impossible for a shortcut
                        self.exposed[new].add(tuple(current))
                    
                elif not self.map[new] and not new == prev:
                    move = direction.copy()
                    
            if np.all(current == self.end): # specifically here because of exposed track calculation
                break
                    
            prev = tuple(current)
            current += move
            self.track.append(tuple(current))

    def gen_cheats(self) -> dict[tuple[Coordinate], int]:
        cheats = defaultdict(list)
        
        for wall, tracks in self.exposed.items():
            if len(tracks) < 2:
                continue

            idx = sorted(self.track.index(t) for t in tracks)
            
            for i in idx[1:]:
                if i - idx[0] - 2: # only consider nonzero
                    cheats[wall].append(i - idx[0] - 2) # dont ask me why, this is an off by 2 error somehow
            
        return Counter(i for saved_list in sorted(cheats.values()) for i in saved_list)

def main(data: str) -> tuple[int]:
    track = Track(data)
    skips = track.gen_cheats()

    return sum(v for k, v in skips.items() if k >= 100)
    
if __name__ == "__main__":
    
    data = """###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..E#...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############"""
    
    
    print(main(data))