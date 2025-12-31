import numpy as np
from typing import Any, Optional, Union
from collections.abc import Callable

##### General 

def recursive_split(data: Any | list[Any], func: Callable = lambda x: x, *delimiters: str) -> list[Any]: 
    if not delimiters:
        return func(data) # consider default lambda x: x if not x.isdigit() else int(x)
    
    return [
        recursive_split(
            i, 
            func, 
            *(delimiters[1:] if type(data) != list else delimiters))
        for i in (data.split(delimiters[0]) if type(data) != list else data)
    ]
    
##### Vectors

def magnitudevec(vector: np.ndarray) -> float:
    return np.sqrt(np.sum(vector ** 2))

def unitvec(vector: np.ndarray) -> np.ndarray:
    return (vector / magnitudevec(vector)).astype(float)

def is_coincident(a: np.ndarray, b: np.ndarray) -> bool: # if vectors are a multiple of one another
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