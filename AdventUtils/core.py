from pathlib import Path
from typing import Any, Optional, List, Union
from collections import defaultdict
from collections.abc import Callable
import inspect
import numpy as np

class Solution:
    def __init__(self, *, test_data: Optional[str] = None, memoization_type: Optional[type] = None) -> None:
        with open(Path(inspect.stack()[1].filename).parent / "input_data.txt", "r") as f:
            self.data = self.parse_input(f.read())
            
        if test_data is not None:
            self.test_data = self.parse_input(test_data)
        
        if memoization_type is not None:
            self.memo = defaultdict(memoization_type)
        else:
            self.memo = dict()
        
    def parse_input(self, data: str) -> List[Any]:
        return data

    def _part_1(self, use_test_data: bool = False):
        return self.part_1(self.data if not use_test_data else self.test_data)

    def _part_2(self, use_test_data: bool = False):
        return self.part_2(self.data if not use_test_data else self.test_data)

    def part_1(self, data: List[Any]) -> Union[int, str]:        
        return
    
    def part_2(self, data: List[Any]) -> Union[int, str]:
        return
    
    def main(self, use_test_data: bool = False) -> tuple[Union[int, str]]:
        return f"Part 1: {self._part_1(use_test_data)}\nPart 2: {self._part_2(use_test_data)}"
    
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