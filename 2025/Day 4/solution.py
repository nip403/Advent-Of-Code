from AdventUtils import *

class Warehouse(Grid):
    def __init__(self, grid_data: list[Union[list[T], np.ndarray]], *, mapping: Mapping[T, N] = None) -> None:
        super().__init__(grid_data, mapping=mapping)
        
        # my solution is done by "shifting" the entire array by every direction and summing, so a layer of padding is needed
        self.grid = np.pad(self.grid, 1)
        
    @property
    def neighbours(self) -> List[List[N]]:
        return sum(np.roll(self.grid, direction, [0, 1]) for direction in ALL_DIRECTIONS)
    
    def count_rolls(self) -> int:
        return np.sum(self.grid)
    
    def __next__(self) -> None:
        self.grid[(self.grid > 0) & (self.neighbours < 4)] = 0

        return self

class Day4(Solution):
    """
        __dict__:
            data
            test_data
            memo
    """

    def __init__(self, *, test_data: Optional[str] = None, memoization_type: Optional[type] = None) -> None:
        super().__init__(test_data=test_data, memoization_type=memoization_type)

    def parse_input(self, data: str) -> None:
        return Warehouse([list(row) for row in data.strip().replace(".", "0").splitlines()], mapping={"0": 0, "@": 1}) # replace is needed for the padding later

    def part_1(self, data: List[Any]) -> Union[int, str]: 
        return np.count_nonzero((data.grid > 0) & (data.neighbours < 4))
    
    def part_2(self, data: List[Any]) -> Union[int, str]: 
        initial_count = data.count_rolls()
        last_count = initial_count
        
        while True:
            next(data)
            
            if last_count == data.count_rolls():
                return initial_count - last_count
            
            last_count = data.count_rolls()

if __name__ == "__main__":
    solution = Day4(
        test_data = """..@@.@@@@.
@@@.@.@.@@
@@@@@.@.@@
@.@@@@..@.
@@.@@@@.@@
.@@@@@@@.@
.@.@.@.@@@
@.@@@.@@@@
.@@@@@@@@.
@.@.@@@.@."""
    )

    print(solution.main(use_test_data=False))