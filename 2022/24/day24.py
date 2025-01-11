from dataclasses import dataclass
import os

def getinput():
    with open(os.path.split(__file__)[0] + "\\input.txt", "r") as f:
        data = f.read().rstrip().split("\n")

    return data

class Grid:
    wind = {
        "<": [-1, 0],
        ">": [1, 0],
        "^": [0, -1],
        "v": [0, 1],
    }

    def __init__(self, grid):
        self.grid = self.parse_txt(grid)
        self.pos = [1, 0] # x, y
        self.end = [len(grid[0]) - 2, len(grid) - 1]
    
    def parse_txt(self, grid):
        out = []

        for y, row in enumerate(grid):
            outrow = []

            for x, tile in enumerate(row):
                outrow.append([] if tile == "." else [tile])

            out.append(outrow)
        
        return out

    def _out_of_bounds(self, x, y):
        return x in [0, len(self.grid[0]) - 1] or y in [0, len(self.grid) - 1]

    def __iter__(self):
        return self

    def __next__(self):
        new = [[[] for _ in range(len(self.grid[0]))] for _ in range(len(self.grid))]

        for y, row in enumerate(self.grid):
            for x, tiles in enumerate(row):
                # wall, start or end
                if self._out_of_bounds(x, y) and len(tiles):
                    new[y][x].append(tiles[0])
                    continue

                # move blizzard
                for tile in tiles:
                    newx = x
                    newy = y

                    if tile in list(self.wind.keys()):
                        translation = self.wind[tile]

                        newx += translation[0]
                        newy += translation[1]

                        if self._out_of_bounds(newx, newy):
                            match tile:
                                case "<":
                                    newx = len(self.grid[0]) - 2
                                case ">":
                                    newx = 1
                                case "^":
                                    newy = len(self.grid) - 2
                                case "v":
                                    newy = 1

                        new[newy][newx].append(tile)
                                    
        self.grid = new[:]

        return self

    def __repr__(self):
        """
        rep = ""

        for i in self.grid:
            for j in i:
                if not len(j):
                    rep += "."
                elif len(j) == 1:
                    rep += j[0]
                else:
                    rep += str(len(j))

            rep += "\n"

        return rep
        """
        rep = ""

        for i in self.grid:
            for j in i:
                if not len(j):
                    rep += " "
                else:
                    rep += "#"

            rep += "\n"

        return rep

    def get_available_moves(self, x, y):
        moves = []

        if not len(self.grid[y][x]):
            moves.append([0, 0])

        if not len(self.grid[y-1][x]):
            moves.append([0, -1])
        
        if y < len(self.grid) - 1 and not len(self.grid[y+1][x]): # issue when start is at initial end
            moves.append([0, 1])

        if not len(self.grid[y][x-1]):
            moves.append([-1, 0])

        if not len(self.grid[y][x+1]):
            moves.append([1, 0])

        return moves

    def bfs(self):
        minute = 0
        tracked = set()
        tracked.add((self.pos[0], self.pos[1]))

        while True:
            new_tracked = set()
            next(self)

            for pos in tracked:
                moves = self.get_available_moves(*pos)

                #print(pos, moves)

                for move in moves:
                    x, y = pos[:]

                    x += move[0]
                    y += move[1]

                    new_tracked.add((x, y))

            minute += 1
            tracked = new_tracked.copy()

            if tuple(self.end) in tracked:
                break

        return minute

def part1():
    grid = Grid(getinput())

    return grid.bfs()

def part2():
    grid = Grid(getinput())
    total = 0

    for _ in range(3):
        total += grid.bfs()
        grid.pos, grid.end = grid.end, grid.pos

    return total
    
if __name__ == "__main__":
    print("Part 1:", part1())
    print("Part 2:", part2())
