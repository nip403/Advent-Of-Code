from pathlib import Path
import numpy as np
#from numba import njit, typeof
#from numba.core import types
#from numba.typed import Dict

np.seterr(all="ignore")
np.set_printoptions(suppress=True)

with open(Path(__file__).parent / "input_data.txt", "r") as f:
    data = f.read()
    
results = {
    0: np.array([1])
}

def get_memoized(stones: np.ndarray) -> np.ndarray: # be needing maximum efficiency
    if stones.size == 0:
        return np.array([], dtype=object)
    
    # return a list of np arrays based on input stones
    keys = np.array(list(results.keys()))
    values = np.array(list(results.values()), dtype=object)
    
    sort_indices = np.argsort(keys)
    sorted_keys = keys[sort_indices]
    sorted_values = values[sort_indices]
    stone_indices = np.searchsorted(sorted_keys, stones)
    return sorted_values[stone_indices]
    
    #return values[idx[stones]]

#@njit
def update(stones: np.ndarray) -> np.array:
    # if the results have already been calculated
    memo_mask = np.isin(stones, np.array(list(results.keys())))
    done, unprocessed = stones[memo_mask], stones[~memo_mask]
    
    # find digits
    digits = np.full_like(unprocessed, 1, dtype=np.int8)
    digits[unprocessed > 0] = np.floor(np.log10(unprocessed[unprocessed > 0])) + 1 # prevent log(0)
    
    # mask for even and odd numbers of digits
    even = np.nonzero(digits % 2 == 0)
    odd = np.nonzero(digits % 2 == 1)
    
    # rule for odd digits
    for o in set(unprocessed[odd]):
        results[o] = np.array([o * 2024], dtype=np.int64)

    # split even digit numbers
    div = (10 ** (digits/2))[even]
    left = unprocessed[even] // div
    right = unprocessed[even] % (left * div)
    
    for i in np.unique(unprocessed[even], return_index=True)[1]:
        results[unprocessed[even][i]] = np.array([left[i], right[i]], dtype=int)

    return np.concatenate([np.atleast_1d(i) for i in [*get_memoized(unprocessed[odd]), left, right, *get_memoized(done)]]).ravel()

class Lineup:
    def __init__(self, stones: list[int]) -> None:
        self.stones = np.array(stones, dtype=np.int64)

    def __iter__(self) -> None:
        return self
        
    def __next__(self) -> None:
        # old implementation without vectorisation for part 1
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
        

        ##self.stones = update(self.stones)

        return self

def main(data: str) -> tuple[int]:    
    stones = Lineup([int(i) for i in data.split()])
    
    #stones = Lineup([125,17])
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