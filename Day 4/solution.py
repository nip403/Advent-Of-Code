from pathlib import Path
import numpy as np
import re

with open(Path(__file__).parent / "input_data.txt", "r") as f:
    data = f.read()

def main(data: str) -> int:
    data = data.split("\n")
    
    # Part 1
    xmas = 0
    
    # horizontal
    for row in data:
        xmas += len(re.findall(r"(?=(XMAS|SAMX))", row))
    
    # vertical
    for row in np.transpose([list(i) for i in data]).tolist():
        xmas += len(re.findall(r"(?=(XMAS|SAMX))", "".join(row)))
    
    # diagonal (\)
    for x in range(len(data[0]) - 3):
        for y in range(len(data) - 3):
            if (data[y][x] + data[y+1][x+1] + data[y+2][x+2] + data[y+3][x+3]) in ["XMAS", "SAMX"]:
                xmas += 1
    
    # diagonal (/)
    for x in range(len(data[0]) - 3):
        for y in range(len(data) - 3):
            if (data[y][x+3] + data[y+1][x+2] + data[y+2][x+1] + data[y+3][x]) in ["XMAS", "SAMX"]:
                xmas += 1
                
    # Part 2
    xmas2 = 0
    
    for x in range(len(data[0]) - 2):
        for y in range(len(data) - 2):
            forward = data[y+2][x] + data[y+1][x+1] + data[y][x+2] # /
            back = data[y][x] + data[y+1][x+1] + data[y+2][x+2]  # \
                
            if (forward in ["MAS", "SAM"]) and (back in ["MAS", "SAM"]):
                xmas2 += 1
            
    return xmas, xmas2

if __name__ == "__main__":
    print(main(data))