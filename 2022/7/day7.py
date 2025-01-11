import os

def getinput():
    with open(os.path.split(__file__)[0] + "\\input.txt", "r") as f:
        data = f.read().rstrip().split("\n")

    return data

class Dir:
    def __init__(self, name, parent):
        self.name = name
        self.parent = parent

        self.subdir = {} # name, obj
        self.files = [] # sizes

    def size(self):
        return sum(self.files) + sum(s.size() for s in self.subdir.values())

    def tally_size_under(self, maxval=100000): # part 1
        total = 0

        # if current + all children under maxvval add to total
        if self.size() <= maxval:
            total += self.size()

        # loop through all children, check above
        for s in self.subdir.values():
            total += s.tally_size_under(maxval)

        return total

    def get_all_dirs(self): # part 2
        dirs = {self: self.size()}

        for name, sub in self.subdir.items():
            dirs = {**dirs, **sub.get_all_dirs()}

        return dirs

    def __repr__(self, level=0):
        out = "\t" * level + self.name + "\n"

        for name, sub in self.subdir.items():
            out += sub.__repr__(level + 1)

        for f in self.files:
            out += "\t" * level + str(f) + "\n"

        return out

def build(root, cmds):
    current = root

    while True:
        if not len(cmds):
            break

        line = cmds.pop(0).split(" ")        

        if line[0] == "$":
            if line[1] == "ls":
                continue
            else:
                if line[2] == "..":
                    current = current.parent
                else:
                    current = current.subdir[line[2]]

        elif line[0] == "dir":
            current.subdir[line[1]] = Dir(line[1], current)

        else: 
            current.files.append(int(line[0]))

    return root

def part1():
    commands = getinput()
    root = build(Dir("/", None), commands[1:])

    return root.tally_size_under(100000)

def part2():
    total = 70000000
    target_free = 30000000

    commands = getinput()
    root = build(Dir("/", None), commands[1:])
    occupied = root.size()
    to_empty = occupied - (total - target_free) # find smallest dir above this size

    all_dirs = root.get_all_dirs()

    for i in sorted(all_dirs.values()):
        if i >= to_empty:
            return i

if __name__ == "__main__":
    print("Part 1:", part1())
    print("Part 2:", part2())
