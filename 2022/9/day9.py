import math
import os

def getinput():
    with open(os.path.split(__file__)[0] + "\\input.txt", "r") as f:
        data = f.read().rstrip().split("\n")

    return data

class Vector:
    def __init__(self, x, y):
        self.x = int(x)
        self.y = int(y)

    def __add__(self, vec):
        return Vector(self.x + vec.x, self.y + vec.y)

    def __sub__(self, vec):
        return Vector(self.x - vec.x, self.y - vec.y)
    
    def __repr__(self):
        return f"({self.x}, {self.y})"

    @property
    def vector(self):
        return [self.x, self.y]

    def tail_move(self, diff):
        # doesn't need to move
        if all(abs(i) <= 1 for i in diff.vector):
            return Vector(0, 0)

        # if 2 steps directly across, move in direction by one step
        if abs(diff.x) == 2 and not diff.y:
            return Vector(diff.x//2, 0)

        elif abs(diff.y) == 2 and not diff.x:
            return Vector(0, diff.y//2)

        # not touching and not in same row or column
        else:
            # move 1 unit both axes in direction of diff vector
            return Vector(math.copysign(1, diff.x), math.copysign(1, diff.y))

direction_vec = {
    "R": Vector(1, 0),
    "L": Vector(-1, 0),
    "U": Vector(0, 1),
    "D": Vector(0, -1),
}

def calc_move(head, tail, direction, amount):
    vec = direction_vec[direction]
    tail_moves = set()

    for _ in range(amount):
        head = head + vec
        difference = head - tail
        move = difference.tail_move(difference)
        tail = tail + move
        tail_moves.add(tuple(tail.vector))

    return head, tail, tail_moves

def part1():
    data = getinput()
    tail_coords = set()
    head, tail = Vector(0, 0), Vector(0, 0)

    tail_coords.add(tuple(tail.vector))

    # head and tail overlap at (x=0, y=0) cartesian coords
    for move in data:
        direction, amount = move.split(" ")

        head, tail, current_turn_tail = calc_move(head, tail, direction, int(amount))
        
        for turn in current_turn_tail:
            tail_coords.add(turn)

    return len(tail_coords)

def calc_rope_move(rope, direction, amount):
    tail_coords = set()
    
    for _ in range(amount):
        # move head
        vec = direction_vec[direction]
        rope[0] = rope[0] + vec

        # move rest of rope
        for i in range(len(rope) - 1):
            head, tail = rope[i], rope[i+1]

            difference = head - tail
            move = difference.tail_move(difference)
            tail = tail + move

            rope[i] = head
            rope[i+1] = tail

            if i == 8:
                tail_coords.add(tuple(tail.vector))

    return rope, tail_coords

def display(rope):
    rope = [i.vector for i in rope]
    for y in range(-10, 11):
        out = ""
        for x in range(-10, 11):
            char = ". "
            
            if [x, y] in rope:
                char = str(rope.index([x,y])) + " "

            out += char
        print(out)

def part2():
    data = getinput()
    tail_coords = set()
    rope = [Vector(0, 0) for _ in range(10)]

    tail_coords.add(tuple(rope[-1].vector))

    for move in data:
        direction, amount = move.split(" ")

        rope, current_turn_tail = calc_rope_move(rope, direction, int(amount))
        
        for turn in current_turn_tail:
            tail_coords.add(turn)

    return len(tail_coords)

if __name__ == "__main__":
    print("Part 1:", part1())
    print("Part 2:", part2())
