import os

def getinput():
    with open(os.path.split(__file__)[0] + "\\input.txt", "r") as f:
        calories = [sum(list(map(int, s.rstrip("\n").split("\n")))) for s in f.read().split("\n\n")]
        
    return calories

def part1():
    calories = getinput()
    most = max(calories)

    return most, calories.index(most)

def part2():
    calories = getinput()
    top3 = []

    for _ in range(3):
        most = max(calories)
        pos = calories.index(most)
        top3.append(calories.pop(pos))

    return sum(top3)

if __name__ == "__main__":
    print("Part 1:", part1())
    print("Part 2:", part2())
