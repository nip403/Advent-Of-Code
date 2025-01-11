from AdventUtils import *

class Day25(Solution):
    """
        __dict__:
            data
            test_data
            memo
    """
    
    def __init__(self, *, test_data: Optional[str] = None, memoization_type: Optional[type] = None) -> None:
        self.mapping = {
            "#": 1,
            ".": 0,
        }
        
        super().__init__(test_data=test_data, memoization_type=memoization_type)
        
    def parse_input(self, data: str) -> None:
        schematics = [np.array(list(map(list, i.splitlines())), dtype=str) for i in data.split("\n\n")]
        data = {"keys": [], "locks": []}
        
        self.lock_height = schematics[0].shape[0]
        
        for grid in schematics:
            data["keys" if "".join(grid[0]) == "." * 5 else "locks"].append(
                np.array(["".join(row).count("#") for row in grid.transpose()]) - 1
            )
            
        return data

    def part_1(self, data: List[Any]) -> Union[int, str]: 
        valid = 0
        
        for k in data["keys"]:
            for l in data["locks"]:
                if np.all(k+l <= self.lock_height - 2):
                    valid += 1
        
        return valid
    
    def part_2(self, data: List[Any]) -> Union[int, str]: 
        return True

if __name__ == "__main__":
    solution = Day25(
        test_data = """#####
.####
.####
.####
.#.#.
.#...
.....

#####
##.##
.#.##
...##
...#.
...#.
.....

.....
#....
#....
#...#
#.#.#
#.###
#####

.....
.....
#.#..
###..
###.#
###.#
#####

.....
.....
.....
#....
#.#..
#.#.#
#####"""
    )

    print(solution.main(use_test_data=False))