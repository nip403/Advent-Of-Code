from pathlib import Path
import numpy as np

with open(Path(__file__).parent / "input_data.txt", "r") as f:
    data = f.read()

class Angle:
    def __init__(self, initial: int = 0) -> None: # define a cycle for the direction of the guard's movement
        self._angle = initial
        
    def __iter__(self):
        return self
    
    def __next__(self):
        self._angle += 1
        return self    
    
    @property
    def angle(self) -> float:
        return {
            0: np.pi / 2,     # up
            1: 0,             # right
            2: 3 * np.pi / 2, # down
            3: np.pi,         # left
        }[self._angle % 4]
        
    @property
    def direction(self) -> str:
        return {
            0: "UP",  
            1: "RIGHT",
            2: "DOWN", 
            3: "LEFT", 
        }[self._angle % 4]

    @property
    def vector(self) -> np.array: # returns [dy, dx]
        return np.array([
            -round(np.sin(self.angle)), 
            round(np.cos(self.angle))
        ])

class Map:
    def __init__(self, initial_state: str) -> None:        
        self.state = np.array([
            [
                {
                    ".": 0, # empty/unvisited
                    "#": -1, # obstacle
                    "^": 1, # guard/visited
                }[j]
                for j in list(i)
            ] 
            for i in initial_state.splitlines()
        ])
        
        self.guard = np.array(divmod(
            initial_state.replace("\n", "").index("^"), # index gives (n * y) + x, where n is the length of a row
            len(self.state[0])
        )) # [y (row), x (col)]
        
        self.direction = Angle()
        
    def __iter__(self):
        return self
    
    def __next__(self):
        new = self.guard + self.direction.vector
        
        # check out of bounds, raise (we're done)
        if not (0 <= new[0] < self.state.shape[0] and 0 <= new[1] < self.state.shape[1]):
            raise StopIteration
        
        if self.state[tuple(new)] == -1: # if next position is an obstacle, update direction
            next(self.direction)
        
        else: # otherwise, move and update board
            self.guard = new
            self.state[tuple(self.guard)] = 1
        
        return self
    
    def __str__(self) -> str:
        state = "\n".join(
            "".join(
                "!" if y == self.guard[0] and x == self.guard[1] else {
                    0: ".",  # empty/unvisited
                    -1: "#",  # obstacle
                    1: "X",  # guard/visited
                }[val] 
                for x, val in enumerate(row)
            )
            for y, row in enumerate(self.state)
        )
        
        return f"\n<Map(guard={tuple(self.guard)}), direction={self.direction.direction}>\n{state}\n"
    
    @property
    def visited(self) -> int:
        return np.sum(self.state == 1)
    
class ObstructionFinder(Map):
    def __init__(self, initial_state: str):
        

def main(data: str) -> list[int]:
    state = Map(data)
    
    # Part 1
    while True:
        try:
            next(state)
            #print(state)
            
        except StopIteration:
            break
        
    return state.visited

if __name__ == "__main__":
    print(main(data))