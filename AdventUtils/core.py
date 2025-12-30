from pathlib import Path
from typing import Any, Optional, List, Union
from collections import defaultdict
import inspect

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
    
