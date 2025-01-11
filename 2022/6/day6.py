import os

def getinput():
    with open(os.path.split(__file__)[0] + "\\input.txt", "r") as f:
        data = f.read().rstrip()

    return data

def find_marker(stream, num_chars=4):
    unique = []

    for p, i in enumerate(stream):
        unique.append(i)

        if len(set(unique)) == num_chars:
            return p + 1

        if len(unique) == num_chars:
            unique.pop(0)

    return

def part1():
    stream = getinput()
    
    return find_marker(stream, 4)

def part2():
    stream = getinput()

    return find_marker(stream, 14)

if __name__ == "__main__":
    print("Part 1:", part1())
    print("Part 2:", part2())
