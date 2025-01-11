import numpy as np

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
        self.initial = np.array(divmod( # for part 2
            initial_state.replace("\n", "").index("^"),
            len(self.state[0])
        ))
        
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
    
class ObstructionFinder:
    def __init__(self, state: Map) -> None: # state must be finished iterating!!    
        # find all tiles which are traversed (ignore all that are never touched)
        self.initial_guard = tuple(state.initial)
            
        # find all obstacles & bounds
        self.obstacles = set()
        
        for y in range(len(state.state)):
            for x in range(len(state.state[y])):
                if state.state[y, x] == -1:
                    self.obstacles.add((y, x))
                    
        self.y_bound, self.x_bound = state.state.shape 
        
        # find all possible candidates for obstacles
        self.visited = set()
        for y in range(len(state.state)):
            for x in range(len(state.state[y])):
                if state.state[y, x] == 1:
                    self.visited.add((y, x))
                            
    def simulate(self, obstacle: tuple[int]) -> int: 
        # reset state
        obstacles = self.obstacles | {obstacle}
        
        visited = set((*self.initial_guard, 1)) # set of tuples (y, x, direction % 4)
        guard = np.array(self.initial_guard)
        direction = Angle()
        
        while True:
            new = guard + direction.vector
            
            if new[0] >= self.y_bound or new[1] >= self.x_bound or new[0] < 0 or new[1] < 0:
                return 0
            
            if tuple(new) in obstacles:
                next(direction)
                continue
            
            if (*new, direction._angle % 4) in visited:
                return 1
            
            guard = new.copy()
            visited.add((*guard, direction._angle % 4))
        
    @property
    def candidates(self) -> int: # extremely slow, took ~2.5 mins for me
        return sum(self.simulate(candidate) for candidate in self.visited - {self.initial_guard})
    