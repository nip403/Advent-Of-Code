import numpy as np
from typing import Any, Optional, Union, List
from collections.abc import Callable

##### General 

# would be much easier with regex
def recursive_split(data: Any | list[Any], func: Callable | None, *delimiters: str) -> list[Any]: 
    if not delimiters:
        if func is None:
            func = lambda x: x # consider default lambda x: x if not x.isdigit() else int(x)
            
        return func(data) 
    
    return [
        recursive_split(
            i, 
            func, 
            *(delimiters[1:] if type(data) != list else delimiters))
        for i in (data.split(delimiters[0]) if type(data) != list else data)
    ]
    
def string_multi_replace(data: str, to_remove: str | List[str]) -> str:
    return data if not to_remove else string_multi_replace(data.replace(to_remove[0], ""), to_remove[1:])
    
##### Linear Algebra

def find_pivots(augmented_matrix: np.ndarray) -> List[int]: # assumes in rref, ignores last column
    pivots = []
    free_variables = []
    r = 0
    
    for c in range(augmented_matrix.shape[1] - 1):
        if r >= augmented_matrix.shape[0]:
            free_variables.append(c)
            continue
        
        if augmented_matrix[r, c]:
            pivots.append(c)
            r += 1
            
        else:
            free_variables.append(c)
        
    return pivots, free_variables

def rref_gf2(augmented_matrix: np.ndarray) -> np.ndarray:
    """
    gaussian elimination for galois field 2 GF(2), AOC 2025 Day 10, put here just in case 
    assumes all entries are 0 or 1, probably supports bool too
    solves binary linear systems, use sympy.Matrix.rref for your everyday linear system
    modified & implemented from https://people.math.carleton.ca/~kcheung/math/notes/MATH1107/04/04_gaussian_elimination.html
    """
    
    row = 0
    
    for col in range(augmented_matrix.shape[1] - 1):
        if row >= augmented_matrix.shape[0]:
            break
        
        pivot = row + np.argmax(augmented_matrix[row:, col])
        
        if not augmented_matrix[pivot, col]:
            continue
        
        if pivot != row:
            augmented_matrix[[row, pivot]] = augmented_matrix[[pivot, row]]
            
        for i in range(augmented_matrix.shape[0]):
            if i != row and augmented_matrix[i, col]:
                augmented_matrix[i] ^= augmented_matrix[row] # scaled subtraction is xor in GF(2) 
    
        row += 1
        
    return augmented_matrix
    
##### Vectors

class Vector:
    @classmethod
    def magnitudevec(cls, vector: np.ndarray) -> float:
        return np.sqrt(np.sum(vector ** 2))

    @classmethod
    def unitvec(cls, vector: np.ndarray) -> np.ndarray:
        return (vector / cls.magnitudevec(vector)).astype(float)

    @classmethod
    def is_coincident(cls, a: np.ndarray, b: np.ndarray) -> bool: # if vectors are a multiple of one another
        return abs(1 - ((np.dot(a, b) ** 2) / (np.dot(a, a) * np.dot(b, b)))) < 1e-6 # absolute tolerance, overload with relative in specific cases

##### Quicksort

def cmp(a: int, b: int) -> bool: # is a < b?
        return a < b # define custom compare function
        
def partition(arr: list[int], low: int, high: int, cmp: Optional[Callable] = cmp) -> int:
    pivot = arr[high]
    i = low
    
    for j in range(low, high):
        if cmp(arr[j], pivot):
            arr[i], arr[j] = arr[j], arr[i]
            i += 1
            
    arr[i], arr[high] = arr[high], arr[i]
    return i
        
def quicksort(arr: Union[list[int], np.ndarray], low: int, high: int, *, cmp_function: Optional[Callable] = cmp) -> Union[list[int], np.ndarray]:
    """ 
        In-place Quicksort based on a compare function, 
        which takes 2 args (a, b) and returns True if a should come before b
    """
    
    if low >= high or low < 0:
        return arr
    
    p = partition(arr, low, high, cmp_function)
    
    quicksort(arr, low, p - 1, cmp_function=cmp_function)
    quicksort(arr, p + 1, high, cmp_function=cmp_function)