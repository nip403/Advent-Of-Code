from AdventUtils import *

class Day5(Solution):
    """
        __dict__:
            data
            test_data
            memo
    """

    def __init__(self, *, test_data: Optional[str] = None, memoization_type: Optional[type] = None) -> None:
        super().__init__(test_data=test_data, memoization_type=memoization_type)

    def parse_input(self, data: str) -> None:
        data = data.split("\n\n")
        
        return recursive_split(data[0], int, *"\n-"), recursive_split(data[1], int, "\n")
    
    def part_1(self, data: List[Any]) -> Union[int, str]: 
        ingredients, available = data
        
        return sum(1 for a in available if any(a in range(r[0], r[1]+1) for r in ingredients))    
        
    
    def part_2(self, data: List[Any]) -> Union[int, str]: 
        ingredients = sorted(data[0], key=lambda x: x[0])
        valid = 0
        
        a0, b0 = ingredients[0]
        
        for i in range(1, len(ingredients)):
            a1, b1 = ingredients[i]
            
            if a1 <= b0 + 1:
                b0 = max(b0, b1)
            
            else: # gap found
                valid += b0 - a0 + 1
                a0, b0 = a1, b1  
        
        return valid + b0 - a0 + 1

if __name__ == "__main__":
    solution = Day5(
        test_data = """3-5
10-14
16-20
12-18

1
5
8
11
17
32"""
    )

    print(solution.main(use_test_data=False))