from AdventUtils import *

class Splitter(Grid):
    def __init__(self, grid_data: list[Union[list[T], np.ndarray]], *, mapping: Mapping[T, N] = None, visualise: bool = False) -> None:
        super().__init__(grid_data, mapping=mapping)
        
        self.visualise = visualise
        self.row = 0
        
        self.splits = 0
        self.heads = np.where(self.grid == 2)[1]
        
        self.timelines = np.zeros(self.grid.shape[1])
        self.timelines[self.heads[0]] = 1
        
        print(self.timelines)

    def at_end(self) -> bool:
        return self.row == self.grid.shape[0] - 1
    
    def __next__(self):
        self.row += 1
        
        if not np.any(self.grid[self.row]) and self.visualise:
            self.grid[self.row, self.heads] = 3
        
        else:
            # part 1 - made redundant with part 2 implementation
            for hit in np.intersect1d(np.where(self.grid[self.row] == 1), self.heads):
                self.splits += 1
                self.heads = np.append(
                    self.heads[self.heads != hit], 
                    [hit - 1, hit + 1]
                )
            
            self.heads = np.array(list(set(self.heads)))
            
            # part 2 - keep a row of particle counts at each space, increment only the ones "hit"
            hits = self.grid[self.row] * self.timelines
            self.timelines -= hits
            self.timelines += np.roll(hits, 1) + np.roll(hits, -1)
                        
        return self

class Day7(Solution):
    """
        __dict__:
            data
            test_data
            memo
    """

    def __init__(self, *, test_data: Optional[str] = None, memoization_type: Optional[type] = None) -> None:
        super().__init__(test_data=test_data, memoization_type=memoization_type)

    def parse_input(self, data: str) -> None:
        return Splitter([list(i) for i in data.split("\n")], mapping={".": 0, "^": 1, "S": 2, "|": 3}, visualise=True)

    def part_1(self, data: List[Any]) -> Union[int, str]: 
        while not data.at_end():
            next(data)
        
        return data.splits
    
    def part_2(self, data: List[Any]) -> Union[int, str]: 
        while not data.at_end():
            next(data)
        
        return int(np.sum(data.timelines))

if __name__ == "__main__":
    solution = Day7(
        test_data = """.......S.......
...............
.......^.......
...............
......^.^......
...............
.....^.^.^.....
...............
....^.^...^....
...............
...^.^...^.^...
...............
..^...^.....^..
...............
.^.^.^.^.^...^.
..............."""
    )

    print(solution.main(use_test_data=False))