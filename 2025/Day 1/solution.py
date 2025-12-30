from AdventUtils import *

class Day1(Solution):
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

    def part_1(self, data: List[Any]) -> Union[int, str]: 
        dial = 50
        password = 0

        for instruction in data:
            dial = (dial + ((1 if instruction[0] == "R" else -1) * int(instruction[1:]))) % 100
            
            if not dial:
                password += 1

        return password
    
    def part_2(self, data: List[Any]) -> Union[int, str]:         
        dial = 50
        password = 0

        for instruction in data:
            direction = 1 if instruction[0] == "R" else -1
            
            # Feels like there's something here but I am not bothered to go to this much effort for a day 1 puzzle
            """
            shift = direction * int(instruction[1:])
            new = dial + shift
            password += abs(shift + dial * direction) // 100
            dial = new % 100
            """
            
            for _ in range(int(instruction[1:])):
                dial = (dial + direction) % 100
                password += dial == 0 
            
        return password

if __name__ == "__main__":
    solution = Day1(
        test_data = """L68
L30
R48
L5
R60
L55
L1
L99
R14
L82"""
    )

    print(solution.main())