from pathlib import Path
import numpy as np

with open(Path(__file__).parent / "input_data.txt", "r") as f:
    data = f.read()

UP = np.array([0, -1], dtype=int)
DOWN = np.array([0, 1], dtype=int)
LEFT = np.array([-1, 0], dtype=int)
RIGHT = np.array([1, 0], dtype=int)

class Warehouse:
    def __init__(self, warehouse: str) -> None:
        self.map = np.array([
            [{
                "#": 1,
                "O": 2,
                ".": 0,
                "@": 3,
            }[j] for j in list(i)
            ]
        for i in warehouse.splitlines()
        ])
        
        self.robot = np.ravel(np.where(self.map == 3))
        
    def __str__(self) -> str:
        return "\n".join(["".join(".#O@"[cell] for cell in row) for row in self.map]) 
    
    def move(self, direction: np.ndarray) -> bool:
        current = self.robot.copy()
        move = 0
        
        while True:
            check = current + direction
            
            if not check:
            
            
        print(start, end)
            

def main(data: str) -> tuple[int]:
    data = """########
#..O.O.#
##@.O..#
#...O..#
#.#.O..#
#...O..#
#......#
########

<^^>>>vv<v>>v<<"""




    warehouse, movements = data.split("\n\n")
    movements = np.array([{
        "^": UP,
        "v": DOWN,
        "<": LEFT,
        ">": RIGHT,    
    }[i] for i in list(movements.replace("\n", ""))])
    warehouse = Warehouse(warehouse)
    
    # Part 1
    for m in movements:
        print(warehouse, m)
        warehouse.move(m)

    # Part 2

    return

if __name__ == "__main__":
    print(main(data))