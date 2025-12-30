from AdventUtils import *

class Day3(Solution):
    """
        __dict__:
            data
            test_data
            memo
    """

    def __init__(self, *, test_data: Optional[str] = None, memoization_type: Optional[type] = None) -> None:
        super().__init__(test_data=test_data, memoization_type=memoization_type)

    def parse_input(self, data: str) -> None:
        return data.strip().splitlines()
    
    def maximise_joltage(self, bank: list[int], batteries: int) -> list[int]:
        if batteries == 1:
            return [max(bank)]
        
        largest = max(bank)
        i = bank.index(largest)
        
        # no room for hopecore this is serious stuff
        while len(bank) - i < batteries:
            largest -= 1
            
            try:
                i = bank.index(largest)
            except:
                if not largest:
                    raise Exception("Something went seriously wrong.")
                            
        return [largest] + self.maximise_joltage(bank[i + 1:], batteries - 1)

    def part_1(self, data: List[Any]) -> Union[int, str]:         
        return sum(int("".join(map(str, self.maximise_joltage([int(b) for b in bank], 2)))) for bank in data)
    
    def part_2(self, data: List[Any]) -> Union[int, str]: 
        return sum(int("".join(map(str, self.maximise_joltage([int(b) for b in bank], 12)))) for bank in data)

if __name__ == "__main__":
    solution = Day3(
        test_data = """987654321111111
811111111111119
234234234234278
818181911112111"""
    )

    print(solution.main(use_test_data=False))