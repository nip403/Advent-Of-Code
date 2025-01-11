from pathlib import Path
import numpy as np
import re

with open(Path(__file__).parent / "input_data.txt", "r") as f:
    data = f.read()
    
def row_reduce(matrix: np.ndarray) -> None:
    # reduce to rref - since its only a 2x3 matrix every time, its simpler to just hard code it
    if not matrix[0, 0]:
        matrix = matrix[::-1]
    
    if matrix[0, 0]:
        matrix[0] /= matrix[0, 0]
        
    elif matrix[0, 1]:
        matrix[0] /= matrix[0, 1]
        
    if matrix[1, 0]:
        matrix[1] -= (matrix[1, 0] / matrix[0, 0]) * matrix[0]  
    
    if matrix[1, 1]:
        matrix[1] /= matrix[1, 1]
        
    if matrix[1, 1]:
        matrix[0] -= matrix[0, 1] * matrix[1]
    
def main(data: str) -> tuple[int]:
    machines = [
        [
            np.array([
                k for k in re.split(r":\s|,\s|\n|\+|=", j) if k.isdigit()
            ], dtype=int) 
            for j in i.splitlines()
        ] 
        for i in data.split("\n\n")
    ]
    # Part 1
    tokens = 0
    
    for m in machines:
        augmented = np.column_stack(m).astype(np.float64)    
        row_reduce(augmented)
        
        if np.array_equal(augmented[-1], np.zeros(3, dtype=np.float64)): # infinitely many solutions
            raise
        
            # luckily, all consistent matrices have unique solutions in the dataset 
        
        elif np.array_equal(augmented[-1, :-1], np.zeros(2, dtype=np.float64)): # inconsistent system, no solutions
            continue
        
        elif np.all(np.isclose(augmented[:, -1], np.round(augmented[:, -1]))): # unique solution exists, but first check if they are integer solutions
            tokens += 3 * augmented[0, -1] + augmented[1, -1]
                             
    # Part 2
    tokens_adj = 0
    offset = 10_000_000_000_000
    
    for m in machines:
        augmented = np.column_stack(m).astype(np.float64)  
        augmented[:, -1] += offset  
        row_reduce(augmented)
        
        if np.array_equal(augmented[-1], np.zeros(3, dtype=np.float64)): 
            raise
        
        elif np.array_equal(augmented[-1, :-1], np.zeros(2, dtype=np.float64)):
            continue
        
        elif np.all(np.abs(augmented[:, -1] - np.round(augmented[:, -1])) <= .001): # switch to an absolute tolerance, since floating point comparisons fails breaks down with such large numbers 
            tokens_adj += 3 * augmented[0, -1] + augmented[1, -1]

    return int(tokens), int(tokens_adj)

if __name__ == "__main__":
    print(main(data))