import os

def getinput():
    with open(os.path.split(__file__)[0] + "\\input.txt", "r") as f:
        data = f.read().rstrip().split("\n")

    return data

def get_visible(trees):
    trees = [[[int(t), False] for t in row] for row in trees] # [height, visible? (bool)]

    # edge cases
    for i in range(len(trees[0])):
        trees[0][i][1] = True # top
        trees[-1][i][1] = True # bottom
 
    for i in range(len(trees)):
        trees[i][0][1] = True # left
        trees[i][-1][1] = True # right

    # check all trees inside boundaries
    for y in range(1, len(trees) - 1):
        for x in range(1, len(trees[y]) - 1):
            trees = check_visibility(trees, x, y)

    return trees

def check_visibility(trees, X, Y):
    # counts if visible from ANY direction
    height = trees[Y][X][0]
    visible = False

    # up
    for y in reversed(range(Y)):
        if trees[y][X][0] >= height:
            break
    else: # im sorry
        visible = True

    # down
    for y in range(Y + 1, len(trees)):
        if trees[y][X][0] >= height:
            break
    else:
        visible = True

    # left
    for x in reversed(range(X)):
        if trees[Y][x][0] >= height:
            break
    else:
        visible = True

    # right
    for x in range(X + 1, len(trees[0])):
        if trees[Y][x][0] >= height:
            break
    else:
        visible = True

    trees[Y][X][1] = visible

    return trees

def count_visible(trees):
    count = 0

    for row in trees:
        for t in row:
            if t[1]:
                count += 1

    return count

def part1():
    trees = getinput()
    
    return count_visible(get_visible(trees))

def calc_score(trees, X, Y):
    # if on edge, scenic score = 0
    if X == 0 or Y == 0 or X == len(trees[0]) - 1 or Y == len(trees) - 1:
        return trees

    # note: viewing distance includes tree that is blocking
    height = trees[Y][X][0]
    left = 0
    right = 0
    up = 0
    down = 0

    # up
    for y in reversed(range(Y)):
        up += 1

        if trees[y][X][0] >= height:
            break
    
    # down
    for y in range(Y + 1, len(trees)):
        down += 1

        if trees[y][X][0] >= height:
            break

    # left
    for x in reversed(range(X)):
        left += 1

        if trees[Y][x][0] >= height:
            break

    # right
    for x in range(X + 1, len(trees[0])):
        right += 1

        if trees[Y][x][0] >= height:
            break

    trees[Y][X][1] = left * right * up * down

    return trees

def part2():
    trees = [[[int(t), 0] for t in row] for row in getinput()] # [height, scenic score]

    for y in range(len(trees)):
        for x in range(len(trees[y])):
            trees = calc_score(trees, x, y)

    return max(max(tree[1] for tree in row) for row in trees)

if __name__ == "__main__":
    print("Part 1:", part1())
    print("Part 2:", part2())
