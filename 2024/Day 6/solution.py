from pathlib import Path

from utils import Map, ObstructionFinder

with open(Path(__file__).parent / "input_data.txt", "r") as f:
    data = f.read()

def main(data: str) -> tuple[int]:
    state = Map(data)
    
    # Part 1
    while True:
        try:
            next(state)
            #print(state)
            
        except StopIteration:
            break
        
    obfinder = ObstructionFinder(state)
        
    return state.visited, obfinder.candidates # Part 2

if __name__ == "__main__":
    print(main(data))