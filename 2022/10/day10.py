import os

def getinput():
    with open(os.path.split(__file__)[0] + "\\input.txt", "r") as f:
        data = f.read().rstrip().split("\n")

    return data

def register(instructions):
    X = 1
    cyclenum = 1

    for i in instructions:
        if i == "noop":
            yield X, cyclenum

        else:
            val = int(i.split(" ")[-1])
            yield X, cyclenum

            cyclenum += 1
            yield X, cyclenum
            X += val

        cyclenum += 1

    return X

def part1():
    instructions = getinput()
    total_strength = 0
    desired = [20, 60, 100, 140, 180, 220]

    for val, n in register(instructions):
        if n in desired:
            total_strength += val * n

    return total_strength

def part2():
    instructions = getinput()
    render = " "

    for sprite, cycle in register(instructions):
        if cycle - 1 and not (cycle) % 40:
            render += "\n"

        # current pixel to render
        position = (cycle - 1) % 40

        # draw pixel in position
        # check if pixel drawn is within sprite
        if sprite - 1 <= position <= sprite + 1:
            render += "#"
        else:
            render += " "

    return render

if __name__ == "__main__":
    print("Part 1:", part1())
    print("Part 2:", part2())
