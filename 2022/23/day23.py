import os

# Note: my program is terrible and very slow, please excuse me

def getinput():
    with open(os.path.split(__file__)[0] + "\\input.txt", "r") as f:
        data = f.read().rstrip().split("\n")

    return data

def parse_data(data):
    coords = []

    for y, row in enumerate(data):
        for x, tile in enumerate(row):
            if tile == "#":
                coords.append([x, y])
    
    return Group(coords)

class Group:
    def __init__(self, coords):
        self.elves = coords
        self.order = [1, 2, 3, 4] # north, south, west, east

    def __iter__(self):
        return self

    def __next__(self):
        intended = []

        # check for each elf
        for e in self.elves:
            """
            no_elf_adj = True

            for dx in range(-1, 2):
                for dy in range(-1, 2):
                    if not (dx or dy):
                        continue

                    if [e[0]+dx, e[1]+dy] in self.elves:
                        no_elf_adj = False

            if no_elf_adj:
                intended.append(e)
                continue
            """
            # above is too inefficient, god i hate this should have used complex nums
            if [e[0]-1, e[1]] in self.elves\
                 or [e[0]+1, e[1]] in self.elves\
                 or [e[0], e[1]-1] in self.elves\
                 or [e[0]-1, e[1]-1] in self.elves\
                 or [e[0]+1, e[1]-1] in self.elves\
                 or [e[0], e[1]+1] in self.elves\
                 or [e[0]-1, e[1]+1] in self.elves\
                 or [e[0]+1, e[1]+1] in self.elves:
                intended.append(e)
                continue

            """
        1   If there is no Elf in the N, NE, or NW adjacent positions, the Elf proposes moving north one step.
        2   If there is no Elf in the S, SE, or SW adjacent positions, the Elf proposes moving south one step.
        3   If there is no Elf in the W, NW, or SW adjacent positions, the Elf proposes moving west one step.
        4   If there is no Elf in the E, NE, or SE adjacent positions, the Elf proposes moving east one step.
            """

            for o in self.order:
                if o == 1 and not ([e[0], e[1]-1] in self.elves or [e[0]-1, e[1]-1] in self.elves or [e[0]+1, e[1]-1] in self.elves):
                    intended.append([e[0], e[1]-1])
                    break

                if o == 2 and not ([e[0], e[1]+1] in self.elves or [e[0]-1, e[1]+1] in self.elves or [e[0]+1, e[1]+1] in self.elves):
                    intended.append([e[0], e[1]+1])
                    break

                if o == 3 and not ([e[0]-1, e[1]] in self.elves or [e[0]-1, e[1]-1] in self.elves or [e[0]-1, e[1]+1] in self.elves):
                    intended.append([e[0]-1, e[1]])
                    break
                
                if o == 4 and not ([e[0]+1, e[1]] in self.elves or [e[0]+1, e[1]-1] in self.elves or [e[0]+1, e[1]+1] in self.elves):
                    intended.append([e[0]+1, e[1]])
                    break
            else:
                intended.append(e) 
                
        # find conflicting dest and add to ban list
        seen = []
        ban = []

        for c in intended:
            if c in seen:
                ban.append(c)
            else:
                seen.append(c)

        # move elves
        for p, i in enumerate(intended):
            if i in ban:
                intended[p] = self.elves[p]

        # part 2, this is broken
        self.new_prop = False

        for i in range(len(intended)):
            if not intended[i] == self.elves[i] and not intended[i] in ban:
                self.new_prop = True 
                break

        self.elves = intended[:]

        # change priority of checking
        self.order.append(self.order.pop(0))

        return self

    def __repr__(self):
        out = ""
        minx = min(e[0] for e in self.elves)
        miny = min(e[1] for e in self.elves)
        maxx = max(e[0] for e in self.elves)
        maxy = max(e[1] for e in self.elves)

        # translate minx, miny to 0, 0
        for y in range(maxy - miny + 1):
            for x in range(maxx - minx + 1):
                if [x+minx, y+miny] in self.elves:
                    out += "#"
                else:
                    out += "."

            out += "\n"

        return out

def part1():
    elves = parse_data(getinput())

    for _ in range(10):
        next(elves)

    """
    minx = min(e[0] for e in elves.elves)
    miny = min(e[1] for e in elves.elves)
    maxx = max(e[0] for e in elves.elves)
    maxy = max(e[1] for e in elves.elves)

    return (maxx - minx + 1) * (maxy - miny + 1) - len(elves.elves)
    """

    return elves.__repr__().count(".")

def part2():# this is broken af
    elves = parse_data(getinput()) 
    rounds = 0

    while True:
        next(elves)
        rounds += 1
        print(rounds)

        if not elves.new_prop:
            return rounds
    
if __name__ == "__main__":
    #print("Part 1:", part1())
    print("Part 2:", part2())