import numpy as np

# vector constants
UP = np.array([-1, 0], dtype=int)
DOWN = np.array([1, 0], dtype=int)
LEFT = np.array([0, -1], dtype=int)
RIGHT = np.array([0, 1], dtype=int)
UPLEFT = UP + LEFT
UPRIGHT = UP + RIGHT
DOWNLEFT = DOWN + LEFT
DOWNRIGHT = DOWN + RIGHT

CROSS_DIRECTIONS = [UP, DOWN, LEFT, RIGHT]
ALL_DIRECTIONS = [UP, DOWN, LEFT, RIGHT, UPLEFT, UPRIGHT, DOWNLEFT, DOWNRIGHT]