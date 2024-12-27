from pathlib import Path
import numpy as np
from collections import deque

with open(Path(__file__).parent / "input_data.txt", "r") as f:
    data = f.read()
    
def checksum(arr: list[int]):
    total = 0
    
    for pos, file_id in enumerate(arr):
        if file_id == -1:
            continue
        
        total += pos * int(file_id) # ok why does np only go up to int64...
        
    return total

def print_storage(storage: np.array) -> None:
    print("".join(["." if i == -1 else str(i) for i in storage.tolist()]))

def main(data: str) -> tuple[int]:    
    # translate dense file representation
    data = [int(i) for i in data]
    file_id = -1
    storage = np.empty(sum(data), dtype=int)
    idx = 0
    free = deque()
    
    for i, length in enumerate(data):
        if not i % 2:
            file_id += 1
            storage[idx: idx + length] = file_id
            
        else:
            free.extend(range(idx, idx + length))
            storage[idx: idx + length] = -1
            
        idx += int(length)

    storage2 = storage.copy()

    # Part 1
    i = len(storage)
    num_free = len(free)
    
    while True:
        i -= 1
        #print_storage(storage)
        
        if all(storage[-num_free:] == -1):
            break
        
        if storage[i] == -1:
            continue
        
        storage[free.popleft()] = storage[i]
        storage[i] = -1
        
    # Part 2 - holy off-by-one errors, i hate it so much
    snapshot_free = data[1::2] # lengths of free spaces
    affected = {} # tracks amounts used in each of the free spaces
    
    for f in reversed(range(1, file_id + 1)):
        length = data[f*2] # length of file to move
        
        for i, spaces in enumerate(snapshot_free[:f]): # attempt to move within data[:2*f] (i.e. all spaces "before" the file)
            if spaces >= length:
                snapshot_free[i] -= length # "uses up" part of free space
                storage2[sum(data[:2*i + 1]) + affected.get(i, 0): sum(data[:2*i + 1]) + length + affected.get(i, 0)] = f # the section of free space that is used by, offset by the amount in this free space that is already used up
                storage2[sum(data[:2*f]): sum(data[:2*f]) + length] = -1 # remove file from original spaces
                
                if i in affected.keys(): # if the initially empty space was partially populated and has space for more, we need to offset by the amount already filled
                    affected[i] += length
                else:
                    affected[i] = length 
                    
                break
    
        #print_storage(storage2)

    return checksum(storage), checksum(storage2)

if __name__ == "__main__":
    print(main(data))