from pathlib import Path
import math

with open(Path(__file__).parent / "input_data.txt", "r") as f:
    data = f.read()

class Lineup:
    def __init__(self, stones: list[int]) -> None:
        self.stones = stones
        self.memo = {}
        self.levels = {} # for debugging
        
    def update(self, value: int, remaining: int) -> int:
        # for debugging
        if not remaining in self.levels:
            self.levels[remaining] = [value]
        else:
            self.levels[remaining].append(value)
        
        if not remaining:
            return 1
        
        if (value, remaining) in self.memo:
            return self.memo[(value, remaining)]
        
        # 0 -> 1
        if not value:
            return self.memo.setdefault((value, remaining), self.update(1, remaining - 1))
        
        # even digits
        digits = math.floor(math.log10(value)) + 1
        div = 10 ** (digits // 2)

        if not digits % 2:
            return self.memo.setdefault((value, remaining), (self.update(left := value // div, remaining - 1) + self.update(value % (left * div), remaining - 1)))
        
        # i *= 2024
        return self.memo.setdefault((value, remaining), self.update(value * 2024, remaining - 1))
    
    def blink(self, num_blinks: int) -> int:
        return sum(self.update(s, num_blinks) for s in self.stones)

def main(data: str) -> tuple[int]:    
    stones = Lineup([int(i) for i in data.split()])

    return stones.blink(25), stones.blink(75)

if __name__ == "__main__":
    print(main(data))