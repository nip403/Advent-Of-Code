import os

"""
A X rock      1
B Y paper     2
C Z scissors  3

loss: 0
draw: 3
win:  6
"""

score = {
    0: 3,
    1: 6,
   -2: 6,
   -1: 0,
    2: 0
}

def getinput():
    with open(os.path.split(__file__)[0] + "\\input.txt", "r") as f:
        moves = f.readlines()

    return list(map(lambda x: x.rstrip("\n"), moves))

def calcscore(move):
    return score[move[1] - move[0]] + move[1]

######################################### PART 2 #########################################

translate_move = {
    "A": 1,
    "B": 2,
    "C": 3,
    "X": 1,
    "Y": 2,
    "Z": 3,
}

"""            my score - opp score
1 beats 3           1 - 3 = -2               win
2 beats 1           2 - 1 =  1               win
3 beats 2           3 - 2 =  1               win

1 beaten by 2       1 - 2 = -1               lose
2 beaten by 3       2 - 3 = -1               lose
3 beated by 1       3 - 1 =  2               lose

when = 0 its a draw
"""

def translate(moves):
    return [[translate_move[m[0]], translate_move[m[-1]]] for m in moves]

def part1():
    moves = [calcscore(i) for i in translate(getinput())]

    return sum(moves)

######################################### PART 2 #########################################
"""
X lose
Y draw
Z win
"""

"""
A rock      1
B paper     2
C scissors  3

loss: 0
draw: 3
win:  6
"""

enemymove = {
    "A": 1,
    "B": 2,
    "C": 3,
}

xyz = {
    "A": [3, 1, 2],
    "B": [1, 2, 3],
    "C": [2, 3, 1],
}

def find_move(move):
    # receive input e.g. "A X"
    index = "XYZ".index(move[-1])

    return [
        enemymove[move[0]], 
        xyz[move[0]][index],
    ]

def translate(moves):
    return [find_move(i) for i in moves]

def part2():
    moves = translate(getinput())

    return sum(calcscore(m) for m in moves)

if __name__ == "__main__":
    print("Part 1:", part1())
    print("Part 2:", part2())
