from pathlib import Path
from collections import defaultdict
import numpy as np

np.set_printoptions(threshold=np.inf, suppress=True, linewidth=np.inf)

with open(Path(__file__).parent / "input_data.txt", "r") as f:
    data = f.read()

def step(secret: np.ndarray) -> np.ndarray:
    secret = ((secret << 6) ^ secret) & 0xFFFFFF
    secret = ((secret >> 5) ^ secret) & 0xFFFFFF
    return ((secret << 11) ^ secret) & 0xFFFFFF

def iter_secret(secret: np.ndarray, num_iterations: int = 1) -> np.ndarray:
    for _ in range(num_iterations):
        secret = step(secret)
        
    return secret

def main(data: str) -> tuple[int]:
    buyers = np.array([int(i) for i in data.splitlines()], dtype=np.int64)
    
    # Part 2
    b = buyers.copy()
    
    steps = 2000
    prices = np.empty((len(b), steps + 1), dtype=int)
    prices[:, 0] = b % 10

    # fill prices
    for s in range(steps):
        b = step(b)
        prices[:, s + 1] = b % 10
        
    diffs = np.diff(prices, axis=1)
    
    # find bananas for all sequences
    bananas = defaultdict(int)
    
    for buyer, d in enumerate(diffs):
        seen = set()
        
        for i in range(diffs.shape[1] - 3):
            sequence = tuple(d[i: i+4])
            
            if sequence in seen:
                continue
            
            bananas[sequence] += prices[buyer, i + 4]
            seen.add(sequence)
                
    return np.sum(iter_secret(buyers, 2000)), max(bananas.values())

if __name__ == "__main__":
    print(main(data))