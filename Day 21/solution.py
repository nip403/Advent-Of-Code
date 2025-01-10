from pathlib import Path
from functools import partial, cache
import numpy as np

with open(Path(__file__).parent / "input_data.txt", "r") as f:
    data = f.read()
    
KEYS = np.array([
    list(i) for i in "789\n456\n123\n 0A".splitlines()
])

DIRS = np.array([
    list(" ^A"),
    list("<v>"),
])

def build_translation(keypad: np.ndarray):
    conv = {}
    
    for i in np.ravel(keypad):
        for j in np.ravel(keypad):
            if not i.strip() or not j.strip():
                continue
            
            a = np.ravel(np.where(keypad == i))
            b = np.ravel(np.where(keypad == j))
            
            # do x movement first then y movement
            presses = "<" * (a - b)[1] + "v" * (b - a)[0] + "^" * (a - b)[0] + ">" * (b - a)[1]
            
            # in case this movement travels off the keypad
            if not keypad[(a[0], b[1])].strip() or not keypad[(b[0], a[1])].strip():
                presses = presses[::-1]
            
            conv[i + j] = presses + "A"
            
    return conv

# some important globals
keys = build_translation(KEYS)
dirs = build_translation(DIRS)

def solve_code(sequence: list[str], num_robots: int) -> int:
    initial = "A" 
    presses = 0
    
    for s in sequence:
        move = keys.get(initial + s, "A")
        presses += solve_directional(move, num_robots)
        initial = s
        
    return presses

@cache
def solve_directional(sequence: list[str], depth: int) -> str:
    if not depth:
        return len(sequence)
    
    initial = "A"
    presses = 0

    for s in sequence:
        move = dirs.get(initial + s, "A")
        presses += solve_directional(move, depth - 1)
        initial = s
        
    return presses

def main(data: str) -> tuple[int]:    
    codes = [list(i) for i in data.splitlines()]
    
    complexity = 0
    complexity2 = 0
    
    for c in codes:
        complexity += solve_code(c, 2) * int("".join(c[:-1]))
        complexity2 += solve_code(c, 25) * int("".join(c[:-1]))

    return complexity, complexity2

if __name__ == "__main__":
    print(main(data))