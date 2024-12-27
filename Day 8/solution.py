from pathlib import Path
import numpy as np
from itertools import combinations
from math import gcd
import sys

np. set_printoptions(threshold=sys. maxsize)

with open(Path(__file__).parent / "input_data.txt", "r") as f:
    data = f.read()

def main(data: str) -> tuple[int]:
    signal_types = set(list(data.replace("\n", "").replace(".", "")))
    signals = {k: i+1 for i, k in enumerate(signal_types)}
    city = np.array([
        [
            signals.get(i, 0) for i in list(line)
        ]
        for line in data.split("\n")
        ]
    )
    antinodes = np.zeros(city.shape, dtype=int)
    antinodes2 = np.zeros(city.shape, dtype=int)
    
    for signal in signals.values():
        for pair in combinations(np.argwhere(city == signal), 2): # find all pairs of antenna indices for each signal type
            vector = pair[0] - pair[1] # vector going from pair[1] to pair[0]

            # Part 1
            for potential in [pair[0] + vector, pair[1] - vector]:
                if (0 <= potential[0] < city.shape[0]) and (0 <= potential[1] < city.shape[0]):
                    antinodes[*potential] = 1

            # Part 2
            if not any(vector == 0):
                vector //= gcd(*vector) # exactly in line
            
            for direction in [-1, 1]:
                current = pair[0].copy()
                
                while (0 <= current[0] < city.shape[0]) and (0 <= current[1] < city.shape[0]):
                    antinodes2[*current] = 1
                    current += vector * direction

    return np.sum(antinodes == 1), np.sum(antinodes2 == 1)

if __name__ == "__main__":
    print(main(data))