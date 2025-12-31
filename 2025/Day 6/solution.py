from AdventUtils import *

class Day6(Solution):
    """
        __dict__:
            data
            test_data
            memo
    """

    def __init__(self, *, test_data: Optional[str] = None, memoization_type: Optional[type] = None) -> None:
        super().__init__(test_data=test_data, memoization_type=memoization_type)

    def parse_input(self, data: str) -> None:
        return data

    def part_1(self, data: List[Any]) -> Union[int, str]: 
        *nums, ops = np.array([" ".join(i.split()).split() for i in data.strip().split("\n")])
        nums = np.transpose(nums).astype(int)
        
        return np.sum(np.prod(nums[ops == "*"], axis=1)) + np.sum(nums[ops == "+"])
    
    def part_2(self, data: List[Any]) -> Union[int, str]: 
        *nums, ops = data.split("\n")
        
        nums = np.char.strip(np.array([list(i) for i in nums]).T)
        ops = np.array(list("".join(ops.split(" "))))
        
        strings = ["".join(row).strip() for row in nums]
        blocks = np.array([list(map(int, block)) for key, block in it.groupby(strings, key=lambda x: not x) if not key], dtype=object)

        # reduceat is too much work
        return sum(prod(i) for i in blocks[ops == "*"]) + np.sum(np.concatenate(blocks[ops == "+"]))

if __name__ == "__main__":
    solution = Day6(
        test_data = """123 328  51 64 
 45 64  387 23 
  6 98  215 314
*   +   *   +  """
    )

    print(solution.main(use_test_data=False))