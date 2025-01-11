import numpy as np
import os
import re

def getinput():
    with open(os.path.split(__file__)[0] + "\\input.txt", "r") as f:
        data = f.read().rstrip()

    return data.split("\n\n")

def parse_instr(instructions):
    return [list(map(int, re.split("move | from | to ", i)[1:])) for i in instructions.split("\n")]

def get_stacks(text):
    stacks = {}
    text = list(reversed(text.split("\n")))[1:] # get rid of numbers and reverse stacks (top = bottom of stack)
    text = ["".join([i for p, i in enumerate(row) if (p+1) % 4]) for row in text] # get rid of spaces between columns
    text = [row.replace("   ", "[ ]")[1:-1] for row in text] 
    text = np.array([row.split("][") for row in text]).T # bruh finally
    #text = [list(stack) if not "" in stack else list(stack)[:np.where(stack == "")[0][0]] for stack in np.array(text).T]

    for p, i in enumerate(text):
        stacks[p+1] = []

        for crate in i:
            if crate == " ":
                break

            stacks[p+1].append(crate)

    return stacks

def rearrange(stacks, instruction):
    amount, start, end = instruction

    for _ in range(amount):
        stacks[end].append(stacks[start].pop())

    return stacks

def print_stacks(stacks):
    for k, v in stacks.items():
        print(k, " ".join(v), sep=" : ")
    print()

def part1():
    stacks, instructions = getinput()
    moves = parse_instr(instructions)
    stacks = get_stacks(stacks)

    for instruction in moves:
        stacks = rearrange(stacks, instruction)

    return "".join([" " if not len(stacks[i]) else stacks[i][-1] for i in range(1, 10)])

def rearrange_part2(stacks, instruction):
    amount, start, end = instruction

    """ too inefficient
    tmp = stacks[start]

    stacks[end] += tmp[amount:]
    stacks[start] = tmp[:len(tmp) - amount]
    """

    toadd = []

    for _ in range(amount):
        toadd.insert(0, stacks[start].pop())
    
    stacks[end] += toadd

    return stacks

def part2():
    stacks, instructions = getinput()
    moves = parse_instr(instructions)
    stacks = get_stacks(stacks)

    for instruction in moves:
        stacks = rearrange_part2(stacks, instruction)

    return "".join([" " if not len(stacks[i]) else stacks[i][-1] for i in range(1, 10)])

if __name__ == "__main__":
    print("Part 1:", part1())
    print("Part 2:", part2())
