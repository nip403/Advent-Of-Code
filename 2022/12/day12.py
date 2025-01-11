import os

def getinput():
    with open(os.path.split(__file__)[0] + "\\input.txt", "r") as f:
        data = f.read().rstrip().split("\n")

    return data

def process_input(data):
    heightmap = []

    for y, row in enumerate(data):
        current = []

        for x, h in enumerate(row):
            if h == "S":
                h = "a"
                start = [x, y]

            elif h == "E":
                h = "z"
                end = [x, y]
            
            h = ord(h) - ord("a")
            current.append(h)
        heightmap.append(current)

    return heightmap, start, end

direction = {
    0: [0, -1], # up
    1: [0, 1], # down
    2: [-1, 0], # left
    3: [1, 0], # right
}

class Node:
    def __init__(self, x, y, h):
        self.x = x
        self.y = y
        self.h = h
        self.to = []
        self.explored = False
        self.parent = None

    def __repr__(self):
        return f"({self.x}, {self.y})"

def build_graph(heightmap, part2=False):
    heights = [[Node(x, y, h) for x, h in enumerate(row)] for y, row in enumerate(heightmap)]

    # connect nodes
    for y, row in enumerate(heightmap):
        for x, h in enumerate(row):
            for i in range(4):
                _x = x + direction[i][0]
                _y = y + direction[i][1]

                # out of bounds
                if not 0 <= _x < len(heightmap[0]) or not 0 <= _y < len(heightmap):
                    continue

                if not part2:
                    # at most 1 height taller
                    if not heightmap[_y][_x] > h + 1:
                        heights[y][x].to.append(heights[_y][_x])
                else:
                    # can climb from next tile to current i.e. if current at most than 1 higher than next
                    if not h > heightmap[_y][_x] + 1:
                        heights[y][x].to.append(heights[_y][_x])
                
    return heights    

def gen_paths(heightmap, start, end, part2=False): # breadth first search
    heights = build_graph(heightmap, part2)
    node = heights[start[1]][start[0]]
    node.explored = True

    queue = [node]

    while len(queue):
        current = queue.pop(0)

        if (not part2 and current.x == end[0] and current.y == end[1]) or (part2 and not current.h):
            return current

        for e in current.to:
            if not e.explored:
                e.explored = True
                e.parent = current
                queue.append(e)

    return None

def count_steps(endnode: Node) -> int:
    count = 0

    while not endnode.parent is None:
        #print(endnode.x, endnode.y)
        endnode = endnode.parent
        count += 1
    
    return count

def part1():
    end = gen_paths(*process_input(getinput()))

    return count_steps(end)

def part2():
    heightmap, _, end = process_input(getinput())
    node = gen_paths(heightmap, end, [], part2=True) # breadth first search from end, needed to modify graph generation and bfs algo
    
    return count_steps(node)

if __name__ == "__main__":
    print("Part 1:", part1())
    print("Part 2:", part2())