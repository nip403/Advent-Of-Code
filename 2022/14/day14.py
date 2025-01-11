import math
import os

def getinput():
    with open(os.path.split(__file__)[0] + "\\input.txt", "r") as f:
        data = f.read().rstrip().split("\n")

    return data

def parse_input(rocks):
    rocks = [[[int(i) for i in rock.split(",")] for rock in row.split(" -> ")] for row in rocks]
    all_rocks = set()

    for formation in rocks:
        # 498,4 -> 498,6 -> 496,6
        x, y = formation.pop(0)
        all_rocks.add((x, y))

        for new in formation:
            if new[0] == x: # move y
                y_dir = int(math.copysign(1, new[1] - y))
                
                while not y == new[1]:
                    y += y_dir
                    all_rocks.add((x, y))

            elif new[1] == y: # move x
                x_dir = int(math.copysign(1, new[0] - x))
                
                while not x == new[0]:
                    x += x_dir
                    all_rocks.add((x, y))
                
    return all_rocks

class Formation:
    def __init__(self, rock_coords):
        self.rock_coords = rock_coords
        self._build()

    def _build(self):
        self.left = min(r[0] for r in self.rock_coords) - 150 # for part 2 expand the floor
        self.right = max(r[0] for r in self.rock_coords) + 150 
        self.height = max(r[1] for r in self.rock_coords) # end part 1 once sand y coord >= this

        # 0 air, 1 rock, 2 sand
        self.grid = [
            [
                1 if (x, y) in self.rock_coords else 0 for x in range(self.left, self.right + 1)
            ] for y in range(self.height + 1)
        ]

    def add_floor(self):
        self.height += 2
        self.grid.append([0] * len(self.grid[0]))
        self.grid.append([1] * len(self.grid[0]))

    def calc_path(self):
        x = 500 - self.left
        y = 0

        while True:
            if y >= self.height:
                return [x, y]

            # first try moving down 1
            y += 1

            # check below
            if not self.grid[y][x]:
                continue

            # check down left
            elif not self.grid[y][x-1]:
                x -= 1
                continue

            # check down right
            elif not self.grid[y][x+1]:
                x += 1
                continue

            # sand can't move, end path creation
            else:
                return [x, y-1]

    def still_holding(self): # calculates path of next grain and determines if end y coord >= height
        end = self.calc_path()

        return end[1] < self.height
        
    def blocked_source(self):
        end = self.calc_path()

        return end == [500 - self.left, 0]

    def __repr__(self):
        out = str(self.left) + "\n"

        for y in self.grid:
            row = ""

            for x in y:
                row += {
                    0: ".",
                    1: "#",
                    2: "o",
                }[x]
            out += row + "\n"

        return out

    def __iter__(self):
        return self

    def __next__(self):
        end = self.calc_path()

        self.grid[end[1]][end[0]] = 2 # end needs to be translated to match array coords

        return self

def part1():
    rocks = parse_input(getinput())
    grid = Formation(rocks)
    grains = 0

    while True:
        next(grid)
        grains += 1
        #print(grid)

        if not grid.still_holding():
            break

    return grains + 1

def part2():
    rocks = parse_input(getinput())
    grid = Formation(rocks)
    grid.add_floor()
    grains = 0

    while True:
        next(grid)
        grains += 1
        #print(grid)

        if grid.blocked_source():
            break

    return grains + 1
    
if __name__ == "__main__":
    print("Part 1:", part1())
    print("Part 2:", part2())