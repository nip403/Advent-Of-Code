from pathlib import Path
import re

with open(Path(__file__).parent / "input_data.txt", "r") as f:
    data = f.read()

def main(data: str) -> tuple[int]:
    # Part 1
    total = 0
    mult = lambda a, b: int(a) * int(b)
    
    for i in re.findall(r"mul\(\d+,\d+\)", data): # i hate regex
        total += mult(*i[4:-1].split(","))
    
    # Part 2
    total2 = 0
    enabled = True
    
    for i in re.findall(r"mul\(\d+,\d+\)|do\(\)|don't\(\)", data):
        if i == "do()":
            enabled = True
            continue
        
        elif i == "don't()":
            enabled = False
            continue
        
        if enabled:
            total2 += mult(*i[4:-1].split(","))
            
        print(i, enabled, mult(*i[4:-1].split(",")))
        
    return total, total2

if __name__ == "__main__":
    print(main(data))