from pathlib import Path
from collections import deque
import numpy as np

with open(Path(__file__).parent / "input_data.txt", "r") as f:
    data = f.read()
    
def update(combo: np.ndarray, output: list[int], opcode: int, operand: int, pointer: int) -> int:
    match opcode: # my very first use of match, incredible 
        case 0: # floor divide A by 2 ** combo operand, equiv to bitwise rshift
            combo[4] >>= combo[operand]

        case 1: # xor B with literal operand
            combo[5] ^= operand
            
        case 2: # combo modulo 8 -> B
            combo[5] = combo[operand] % 8

        case 3: # if A is not 0, set pointer to literal operand
            if combo[4]:
                pointer = operand - 2 # offset the pointer increase (not supposed to update after instruction)
                
        case 4: # B xor= C
            combo[5] ^= combo[6]
            
        case 5: # output combo operand mod 8
            output.append(combo[operand] % 8)
            
        case 6: # same as 0, store in B
            combo[5] = combo[4] >> combo[operand]
            
        case 7: # same as 0, store in C
            combo[6] = combo[4] >> combo[operand]
            
        case _:
            raise
        
    return pointer

def gen_output(registers: np.ndarray, program: np.ndarray) -> list[int]:
    pointer = 0
    combo = np.empty(7, dtype=int)
    combo[:] = np.array([0, 1, 2, 3, *registers], dtype=int) # keep track of register values in here, A=4

    output = deque()

    while pointer < program.shape[0]:
        opcode, operand = program[pointer: pointer + 2] # check if out of bounds error arises (pointer should always be at least 2 left from end)
        pointer = update(combo, output, opcode, operand, pointer) + 2
                    
    return output

def backtrack(A: int, prog: list[int], i: int): # got this from the internet after optimised brute force was taking too long
    if i == len(prog):
        return A
    
    for b in range(8):
        if (b ^ ((A << 3) + b >> (b ^ 7))) % 8 == prog[i]: 
            if a := backtrack((A << 3) + b, prog, i + 1):
                return a
    
def main(data: str) -> tuple[int]:
    registers, program = data.split("\n\n")
    registers = np.array([int(i.split(": ")[1]) for i in registers.splitlines()])
    program = np.array([int(i) for i in program.split(": ")[1].split(",")])

    return ",".join(str(i) for i in gen_output(registers, program)), backtrack(0, program[::-1], 0)





if __name__ == "__main__":
    print(main(data)) 