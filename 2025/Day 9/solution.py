from AdventUtils import *
from shapely import Polygon, box

class Day9(Solution):
    def __init__(self, *, test_data: Optional[str] = None, memoization_type: Optional[type] = None) -> None:
        super().__init__(test_data=test_data, memoization_type=memoization_type)

    def parse_input(self, data: str) -> None:
        return np.array(recursive_split(data.strip(), int, *"\n,"))

    def part_1(self, data: List[Any]) -> Union[int, str]: 
        return max([np.prod(np.abs(p1 - p2) + 1) for p1, p2 in combinations(data, 2)])
    
    def part_2(self, data: List[Any]) -> Union[int, str]:         
        poly = Polygon(data)

        return max(
            np.prod(np.abs(p1 - p2) + 1) 
            for p1, p2 in combinations(data, 2) 
            if poly.covers(box(*np.minimum(p1, p2), *np.maximum(p1, p2)))
        )

if __name__ == "__main__":
    solution = Day9(
        test_data = """7,1
11,1
11,7
9,7
9,5
2,5
2,3
7,3"""
    )

    print(solution.main(use_test_data=False))