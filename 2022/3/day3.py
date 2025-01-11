import os

def getinput():
    with open(os.path.split(__file__)[0] + "\\input.txt", "r") as f:
        bags = f.readlines()

    return list(map(lambda x: x.rstrip("\n"), bags))

def splitcompartments(bag):
    return [bag[:len(bag)//2], bag[len(bag)//2:]]

def points(bag, needtosplit=False): 
    if needtosplit:
        bag = splitcompartments(bag)

    outbag = []

    for c in bag: # each compartment
        newcomp = []

        for s in c: # each item
            if s.isupper():
                point = ord(s) - 38
            else:
                point = ord(s) - 96
            
            newcomp.append(point)
        outbag.append(sorted(newcomp))

    return outbag if not needtosplit else outbag[0] + outbag[1]

def findmatching(bag):
    return tuple(set(bag[0]) & set(bag[1]))[0]

def part1():
    bags = [splitcompartments(bag) for bag in getinput()]
    bags = list(map(points, bags))
    matching = [findmatching(bag) for bag in bags]

    return sum(matching)

def findbadge(group):
    return tuple(set(group[0]) & set(group[1]) & set(group[2]))[0]

def part2():
    bags = getinput()
    groups = [bags[i:i+3] for i in range(0, len(bags), 3)]
    groups = [[points(b, True) for b in g] for g in groups]
    badges = [findbadge(g) for g in groups]

    return sum(badges)

if __name__ == "__main__":
    print("Part 1:", part1())
    print("Part 2:", part2())
