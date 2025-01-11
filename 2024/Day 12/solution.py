from pathlib import Path
from collections import defaultdict
import numpy as np

np.set_printoptions(threshold=np.inf)

with open(Path(__file__).parent / "input_data.txt", "r") as f:
    data = f.read()
    
UP = np.array([0, -1], dtype=int)
DOWN = np.array([0, 1], dtype=int)
LEFT = np.array([-1, 0], dtype=int)
RIGHT = np.array([1, 0], dtype=int)

def in_bounds(pos: np.ndarray, plot: np.ndarray) -> bool:
    return 0 <= pos[0] < plot[0] and 0 <= pos[1] < plot[1]

def coincident(a: np.ndarray, b: np.ndarray) -> bool: # fancy maths to check if vectors are a multiple of one another
    return abs(1 - ((np.dot(a, b) ** 2) / (np.dot(a, a) * np.dot(b, b)))) < 1e-6 # idk how good this tolerance is

def main(data: str) -> tuple[int]:   
    # Part 1
    plots = np.array([list(line) for line in data.split("\n")])
    visited = set() # skip over entire regions that have been BFS-ed
    price = 0
    
    # Part 2
    regions = {}

    for y in range(plots.shape[0]):
        for x in range(plots.shape[1]):
            pos = np.array([y, x])
            
            if tuple(pos) in visited:
                continue
            
            sides = [] # list of (cell, direction) for part 2
            
            stack = [pos]
            area = 0
            perimeter = 0
            visited_plot = set() # ensure perimeter "double counting" is allowed for outside/different plots
            
            while stack: # BFS
                current = stack.pop()
                
                if tuple(current) in visited: # skip over already-checked cells
                    continue
                
                visited_plot.add(tuple(current)) # no backing up
                visited.add(tuple(current))
                area += 1
                
                for direction in [UP, DOWN, LEFT, RIGHT]: # check neighbours
                    new = current + direction
                    
                    if not in_bounds(new, plots.shape): # out of bounds = +1 to perimeter
                        perimeter += 1
                        sides.append((current, direction))
                    
                    elif tuple(new) not in visited_plot:
                        if plots[tuple(new)] == plots[tuple(current)] and not tuple(new) in visited_plot: # continue search in the same plot
                            stack.append(new)
                            
                        else: # if checked neighbour is a different plant
                            perimeter += 1
                            sides.append((current, direction))
                            
            regions[(len(regions.keys()), area)] = sides
            price += area * perimeter
            
    # Part 2
    discounted = 0
    
    for k, v in regions.items():
        _, area = k
        sides = 0
        
        # translate into dict
        cells = defaultdict(list)
        
        for cell, direction in v:
            cells[tuple(cell)].append(direction)
        
        # holy nesting
        while True:
            if not cells:
                break
            
            sides += 1 # create a new side
            key = next(iter(cells)) # pop a cell + wall
            anchor = np.array(key)
            wall = cells[key].pop()
            
            if not cells[key]:
                del cells[key] # holy moly a del keyword
            
            for vector in [UP, DOWN, LEFT, RIGHT]: # "walk" along each direction
                cell = anchor.copy()
                
                while True:
                    cell += vector

                    if tuple(cell) in cells:
                        if not any(np.array_equal(cmp, wall) for cmp in cells[tuple(cell)]): # wall ends
                            break
                        
                        else: # wall doesnt end, remove new cell from consideration
                            cells[tuple(cell)] = list(filter(
                                lambda arr: not np.array_equal(arr, wall), 
                                cells[tuple(cell)],
                            ))
                            
                            if not cells[tuple(cell)]:
                                del cells[tuple(cell)]
                                
                    else:
                        break
                                
        
        # calculate num sides
        
        discounted += area * sides
        

    return price, discounted

if __name__ == "__main__":
    print(main(data))