from AdventUtils import *

class Day2(Solution):
    """
        __dict__:
            data
            test_data
            memo
    """

    def __init__(self, *, test_data: Optional[str] = None, memoization_type: Optional[type] = None) -> None:
        super().__init__(test_data=test_data, memoization_type=memoization_type)

    def parse_input(self, data: str) -> None:
        return recursive_split(data.strip(), int, *",-")

    def part_1(self, data: List[Any]) -> Union[int, str]: 
        invalid_sum = 0
        
        for ids in data:
            for i in range(ids[0], ids[1] + 1):
                string = str(i)
                digits = int(np.floor(np.log10(i)) + 1)
                
                if string[:digits//2] * 2 == string:
                    invalid_sum += i
            
        return invalid_sum
    
    def part_2(self, data: List[Any]) -> Union[int, str]: # if only i knew regex
        invalid_sum = 0
        
        for ids in data:
            for i in range(int(ids[0]), int(ids[1]) + 1):
                string = str(i)
                digits = int(np.floor(np.log10(i)) + 1)
                
                for window in range(1, digits // 2 + 1):
                    if digits % window:
                        continue
                    
                    head = string[:window]
                    
                    for j in range(window, digits, window):
                        if head != string[j:j+window]:
                            break
                    else: # for else for readability
                        invalid_sum += i
                        break
                    
        return invalid_sum

if __name__ == "__main__":
    solution = Day2(
        test_data = """11-22,95-115,998-1012,1188511880-1188511890,222220-222224,
1698522-1698528,446443-446449,38593856-38593862,565653-565659,
824824821-824824827,2121212118-2121212124"""
    )

    print(solution.main(use_test_data=False))