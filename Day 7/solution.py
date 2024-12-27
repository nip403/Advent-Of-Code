from pathlib import Path
import itertools as it
import math

with open(Path(__file__).parent / "input_data.txt", "r") as f:
    data = f.read()

def main(data: str) -> tuple[int]: # cant be bothered to improve it using recursion
    data = [[int(j) for j in i.replace(":", "").split()] for i in data.splitlines()]

    # Part 1
    total = 0
    
    for equation in data[:]:
        temp = equation[:]
        result = temp.pop(0)
        
        for oplist in it.product([0, 1], repeat=len(equation)-1):
            oplist = list(oplist)
            eq = temp[:]
            running = eq.pop(0)
            
            while eq:
                new = eq.pop(0)
                
                if oplist.pop(0):
                    running += new
                    
                else:
                    running *= new
                    
            if running == result:
                break
        
        else: # if result was not achieved
            total -= result
            
        total += result

    # Part 2
    total2 = 0
    
    for equation in data[:]:
        temp = equation[:]
        result = temp.pop(0)
        
        for oplist in it.product([0, 1, 2], repeat=len(equation)-1):
            oplist = list(oplist)
            eq = temp[:]
            running = eq.pop(0)
            
            while eq:
                new = eq.pop(0)
                op = oplist.pop(0)
                
                if not op:
                    running += new
                    
                elif op == 1:
                    running *= new
                    
                else:
                    running = (running * (10 ** (int(math.log10(new))+1))) + new
                    
            if running == result:
                break
        
        else: # if result was not achieved
            total2 -= result
        
        total2 += result

    return total, total2

if __name__ == "__main__":
    print(main(data))