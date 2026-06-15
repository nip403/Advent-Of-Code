from AdventUtils import *

class Day12(Solution):
    """
        __dict__:
            data
            test_data
            memo
    """

    def __init__(self, *, test_data: Optional[str] = None, memoization_type: Optional[type] = None) -> None:
        super().__init__(test_data=test_data, memoization_type=memoization_type)

    def parse_input(self, data: str) -> None:
        return recursive_split(data, None, "\n\n", "\n")

    def part_1(self, data: List[Any]) -> Union[int, str]: 
        *presents, regions = data
        
        
        return presents
    
    def part_2(self, data: List[Any]) -> Union[int, str]: 
        return

if __name__ == "__main__":
    solution = Day12(
        test_data = """0:
###
##.
##.

1:
###
##.
.##

2:
.##
###
##.

3:
##.
###
##.

4:
###
#..
###

5:
###
.#.
###

4x4: 0 0 0 0 2 0
12x5: 1 0 1 0 2 2
12x5: 1 0 1 0 3 2"""
    )

    print(solution.main(use_test_data=True))