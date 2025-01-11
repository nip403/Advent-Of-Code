from pathlib import Path
import numpy as np
from functools import partial

with open(Path(__file__).parent / "input_data.txt", "r") as f:
    data = f.read()

def main(data: str) -> tuple[int]: # warning: extremely readable solution!
    # Part 1
    left, right = map(partial(np.array, dtype=int), zip(*[i.split() for i in data.split("\n")]))
    
    # Part 2
    # see return statement
    
    return abs(np.sort(left) - np.sort(right)).sum(), sum([i * (right == i).sum() for i in left])

if __name__ == "__main__":
    print(main(data))