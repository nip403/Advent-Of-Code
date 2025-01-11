import os

def getinput():
    with open(os.path.split(__file__)[0] + "\\input.txt", "r") as f:
        ids = f.read().rstrip()

    return ids.split("\n")

def parseids(raw_ids):
    return [[list(map(int, each.split("-"))) for each in both.split(",")] for both in raw_ids]

def part1():
    ids = parseids(getinput())
    contains = 0

    for pair in ids:
        a, b = pair

        # case for exact same range
        if (not a[0] - b[0]) and (not a[1] - b[1]):
            contains += 1
            continue

        for _ in range(2):
            # if a in b (b contains a)
            if a[0] >= b[0] and a[1] <= b[1]:
                contains += 1
                break

            a, b = b, a
        
    return contains
        
def part2():
    ids = parseids(getinput())
    overlap = 0

    for pair in ids:
        # lazy approach :3
        a = range(pair[0][0], pair[0][1]+1)
        b = range(pair[1][0], pair[1][1]+1)

        if len(set(a) & set(b)):
            overlap += 1

    return overlap

if __name__ == "__main__":
    print("Part 1:", part1())
    print("Part 2:", part2())
