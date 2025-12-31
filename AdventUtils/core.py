from pathlib import Path
from typing import Any, Optional, List, Union
from collections import defaultdict
import inspect

class Solution:
    def __init__(self, *, test_data: Optional[str] = None, memoization_type: Optional[type] = None) -> None:
        self.test_data = test_data
        
        if memoization_type is not None:
            self.memo = defaultdict(memoization_type)
        else:
            self.memo = dict()
        
    def parse_input(self, data: str) -> List[Any]:
        return data

    def part_1(self, data: Any) -> Union[int, str]:        
        return
    
    def part_2(self, data: Any) -> Union[int, str]:
        return
    
    def main(self, use_test_data: bool = False) -> tuple[Union[int, str]]:
        if use_test_data:
            data = self.parse_input(self.test_data)
        else:
            with open(Path(inspect.stack()[1].filename).parent / "input_data.txt", "r") as f:
                data = self.parse_input(f.read())
        
        return f"Part 1: {self.part_1(data)}\nPart 2: {self.part_2(data)}"
    
