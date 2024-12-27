from pathlib import Path
import numpy as np
from numba import njit
import cupy as cp

np.seterr(all="ignore")

with open(Path(__file__).parent / "input_data.txt", "r") as f:
    data = f.read()
    
@njit
def update(stones: np.array) -> np.array:
    digits = cp.floor(cp.log10(stones)).astype(cp.int32) + 1
    even = np.nonzero(digits % 2 == 0)
    odd = np.nonzero(digits % 2 == 1)
    
    stones[odd] *= 2024
    stones[stones == 0] = 1
    
    div = (10 ** (digits/2))[even]
    left = stones[even] // div
    right = stones[even] % (left * div)
    
    return np.concatenate((stones[odd], left, right))

class Lineup:
    def __init__(self, stones: list[int]) -> None:
        self.stones = np.array(stones, dtype=np.int64)
    
        
    def __iter__(self) -> None:
        return self
        
    def __next__(self) -> None:
        # old implementation without vectorisation
        """
        new = []
        
        for s in self.stones:
            if s:
                digits = int(np.log10(s)) + 1
            
            if not s:
                new.append(1)
                
            elif not digits % 2:
                div = 10 ** (digits/2)
                left = s // div
                
                new.append(left)
                new.append(s % (left * div))
                
            else:
                new.append(s * 2024)
            
        self.stones = new[:]
        """

        self.stones = update(self.stones)
        print(self.stones)

        return self

def main(data: str) -> tuple[int]:    
    stones = Lineup([int(i) for i in data.split()])
    
    stones = Lineup([125,17])
    counter = -1
    
    # Part 1
    for _ in range(25):
        counter += 1
        print(counter, len(stones.stones))
        next(stones)
        
    res1 = len(stones.stones)
    print(res1)

    # Part 2
    for _ in range(50):
        print(counter, len(stones.stones))
        counter += 1
        next(stones)

    return res1, len(stones.stones)

if __name__ == "__main__":
    print(main(data))