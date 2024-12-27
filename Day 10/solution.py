from pathlib import Path
import numpy as np

with open(Path(__file__).parent / "input_data.txt", "r") as f:
    data = f.read()

class Map:
    def __init__(self, trail: str) -> None:
        self.trail = np.array(
            [
                [
                    int(j) for j in list(i)
                ] 
            for i in trail.splitlines() 
            ]
        )
        
        self.trailheads = np.transpose(np.where(self.trail == 0))
        self.ends = np.transpose(np.where(self.trail == 9))
        self.scores = np.zeros(len(self.trailheads))
        self.ratings = np.zeros(len(self.trailheads))
        
    def _calc(self, current: list[int], trail: list[list[int]]) -> None:
        if any(all(current == row) for row in self.ends):
            self.instance_scores[tuple(current)] = 1
            self.instance_ratings[tuple(current)] += 1 # thank god my implementation scales
            return
        
        trail = np.append(trail, current)
        
        for delta in [np.array(i) for i in [[1, 0], [-1, 0], [0, 1], [0, -1]]]:
            new = current + delta 
            
            if not (0 <= new[0] < self.trail.shape[0]) or not (0 <= new[1] < self.trail.shape[1]):
                continue

            if self.trail[*new] - self.trail[*current] == 1:
                self._calc(new, trail)
        
    def calc(self) -> None:
        for i, head in enumerate(self.trailheads):
            self.instance_scores = {tuple(i): 0 for i in self.ends}
            self.instance_ratings = {tuple(i): 0 for i in self.ends}
            
            self._calc(head, np.array([]))
            
            self.scores[i] = sum(self.instance_scores.values())
            self.ratings[i] = sum(self.instance_ratings.values())
        
    @property
    def total_trail_score(self) -> int:
        return np.sum(self.scores).astype(int)
    
    @property
    def total_trail_rating(self) -> int:
        return np.sum(self.ratings).astype(int)


def main(data: str) -> tuple[int]:
    trail = Map(data)
    trail.calc()

    return trail.total_trail_score, trail.total_trail_rating

if __name__ == "__main__":
    print(main(data))