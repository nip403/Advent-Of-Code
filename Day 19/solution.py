from pathlib import Path
from collections import defaultdict

with open(Path(__file__).parent / "input_data.txt", "r") as f:
    data = f.read()

def valid_design(towels: list[str], design: str, memo: dict = defaultdict(bool)) -> bool:
    if not design:
        return True
    
    if design in memo:
        return memo[design]
    
    for t in towels:
        if any(c not in design[:len(t)] for c in t): # filter towels with colours not in the design
            continue 
        
        if design.startswith(t):
            if valid_design(towels, design[len(t):], memo):
                return memo.setdefault(design, True)
            
    return memo.setdefault(design, False)
    
def perms(towels: list[str], design: str, memo: dict = defaultdict(int)) -> int:
    if not design:
        return 1
    
    if design in memo:
        return memo[design]
    
    total = 0
    
    for t in towels:
        if any(c not in design[:len(t)] for c in t): # filter towels with colours not in the design
            continue 
        
        if design.startswith(t):
            total += perms(towels, design[len(t):], memo)
            
    return memo.setdefault(design, total)

def main(data: str) -> tuple[int]:
    towels, designs = data.split("\n\n")
    towels = towels.split(", ")
    designs = designs.splitlines()
    
    return sum(valid_design(towels, design) for design in designs), sum(perms(towels, design) for design in designs)

if __name__ == "__main__":
    print(main(data))