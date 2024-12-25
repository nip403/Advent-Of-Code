from pathlib import Path
import numpy as np

with open(Path(__file__).parent / "input_data.txt", "r") as f:
    data = f.read()

def check(l: list[int]) -> int:
    # check if strictly increasing or decreasing
    if not (all(l[i] < l[i + 1] for i in range(len(l) - 1)) or all(l[i] > l[i + 1] for i in range(len(l) - 1))):
        return 0

    # check if all increments are between 1 and 3
    diffs = abs(np.diff(l))
    return np.all((1 <= diffs) & (diffs <= 3))

def check_dampened(l: list[int]) -> int:
    return any(check([element for pos, element in enumerate(l) if not pos == i]) for i in range(len(l))) # O(n^2 log n), incredibly terrible

def main(data: str) -> list[int]:
    # Part 1
    safe = 0
    
    for i in [list(map(int, p.split())) for p in data.split("\n")]:
        safe += check(i)
        
    # Part 2
    damp_safe = 0
    
    for i in [list(map(int, p.split())) for p in data.split("\n")]:
        damp_safe += check_dampened(i)
        
    return safe, damp_safe

if __name__ == "__main__":
    print(main(data))