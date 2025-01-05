from pathlib import Path
import numpy as np
from debug import *

with open(Path(__file__).parent / "input_data.txt", "r") as f:
    data = f.read()

UP = np.array([-1, 0], dtype=int)
DOWN = np.array([1, 0], dtype=int)
LEFT = np.array([0, -1], dtype=int)
RIGHT = np.array([0, 1], dtype=int)

class Warehouse:
    back = ".#O@"
    
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
        return "\n".join(["".join(self.back[cell] for cell in row) for row in self.map]) 
    
    def bounds(self, pos: np.ndarray) -> bool:
        return (0 <= pos[0] < self.map.shape[0]) and (0 <= pos[1] < self.map.shape[1])
    
    def move(self, direction: np.ndarray) -> bool:
        check = self.robot.copy()
        move = [3] # start with robot
        
        while True:
            check += direction
            
            if not (0 <= check[0] < self.map.shape[0] and 0 <= check[1] < self.map.shape[1]): # check bounds 
                return False
            
            if self.map[tuple(check)] == 1: # check walls
                return False
            
            if self.map[tuple(check)] == 2: # continue if obstacle
                move.append(self.map[tuple(check)])
                continue
            
            # encounter an empty space: move entire slice from robot to (current - direction) into robot + direction to current
            for i in move[::-1]:
                self.map[tuple(check)] = i
                check -= direction
                
            self.map[tuple(self.robot)] = 0
            self.robot += direction
            
            return True
        
    def gps_sum(self) -> int:
        gps = 0
        
        for y in range(self.map.shape[0]):
            for x in range(self.map.shape[1]):
                if self.map[y, x] == 2:
                    gps += 100 * y + x
                    
        return gps
    
class WarehouseResized(Warehouse):
    def __init__(self, warehouse: str) -> None:
        super().__init__(warehouse) 
        warehouse = np.zeros((self.map.shape[0], self.map.shape[1] * 2), dtype=int)
        self.back = ".#[@]K" # for printing, "K" is for debugging
        
        for y in range(self.map.shape[0]):
            for x in range(self.map.shape[1]):
                if (v := self.map[y, x]) == 3: # robot
                    warehouse[y, 2 * x: 2 * x + 2] = [3, 0]
                
                elif v == 2:
                    warehouse[y, 2 * x: 2 * x + 2] = [2, 4]
                    
                else:
                    warehouse[y, 2 * x: 2 * x + 2] = [v, v]

        self.map = warehouse
        self.robot = np.ravel(np.where(self.map == 3))
        
    def check_vertical_box_collisions(self, box: list[np.ndarray], direction: np.ndarray) -> bool:
        if not self.bounds(box[0] + direction) or not self.bounds(box[1] + direction):
            return False
        
        left = self.map[tuple(box[0] + direction)] 
        right = self.map[tuple(box[1] + direction)]
        
        if 1 in [left, right]: # walls in the way 
            return False
        
        if left == 2 or right == 4: # box is perfectly aligned vertically
            return self.check_vertical_box_collisions([i + direction for i in box], direction)
        
        moveable = True
        
        # if another box is diagonally colliding to the left
        if left == 4:
            if not self.check_vertical_box_collisions(
                [
                    box[0] + direction + LEFT,
                    box[0] + direction,
                ], 
                direction,
            ):
                moveable = False
            
        # if another box is diagonally colliding to the right
        if right == 2:
            if not self.check_vertical_box_collisions(
                [
                    box[1] + direction,
                    box[1] + direction + RIGHT,
                ], 
                direction,
            ):
                moveable = False
                
        if not left and not right: # both spaces free to move into
            return True

        return moveable
    
    def vertical_to_move(self, pos: np.ndarray, direction: np.ndarray) -> list[np.ndarray]:
        """ Recursively generate a list of coords of box parts to push i.e. shape = [:, 2] in order of first encountered from the robot

        Args:
            pos (np.ndarray): section currently being checked
            direction (np.ndarray): direction of movement
        """
        
        new = pos + direction
        
        if not self.map[tuple(new)]:
            return []
        
        if self.map[tuple(new)] == 2:
            return [
                new,
                new + RIGHT,
            ] + self.vertical_to_move(new, direction) + self.vertical_to_move(new + RIGHT, direction)
            
        elif self.map[tuple(new)] == 4:
            # prevent double counting
            if self.map[tuple(pos)] == 4:
                return []
            
            return [
                new,
                new + LEFT,
            ] + self.vertical_to_move(new, direction) + self.vertical_to_move(new + LEFT, direction)
            
        raise
        
    def move(self, direction: np.ndarray) -> bool:
        check = self.robot.copy()
        delta = 0 # the number of steps to walk from robot to the next empty space
        
        while True:
            check += direction
            delta += 1 
            
            if not (0 <= check[0] < self.map.shape[0] and 0 <= check[1] < self.map.shape[1]): # check bounds 
                return False
            
            if self.map[tuple(check)] == 1: # check walls
                return False
            
            if not self.map[tuple(check)]: # proceed to move everything
                break
            
            # calculate if the boxes can be pushed in vertical direction
            if not (np.array_equal(direction, LEFT) or np.array_equal(direction, RIGHT)): # if its left or right, we only need to keep checking in that direction, which will terminate as usual
                if self.map[tuple(check)] == 2: 
                    if not self.check_vertical_box_collisions(
                        [
                            check,
                            check + RIGHT,
                        ],
                        direction,
                    ):
                        return False
                    
                elif self.map[tuple(check)] == 4:
                    if not self.check_vertical_box_collisions(
                        [
                            check + LEFT, # literally JUST BECAUSE OF THIS, THE FACT I HAD CHECK+LEFT AND CHECK IN THE WRONG ORDER AS THE ONLY BUG, I SPENT 2.5 EXTRA HOURS DEBUGGING EVERYTHING ELSE THAT HAD NO ISSUE
                            check,
                        ],
                        direction,
                    ):
                        return False
                
        # do the moving
        if np.array_equal(direction, LEFT):
            self.map[check[0], check[1]: self.robot[1]] = self.map[check[0], check[1] + 1: self.robot[1] + 1]
            self.map[tuple(self.robot)] = 0
        
        elif np.array_equal(direction, RIGHT):
            self.map[check[0], self.robot[1] + 1: check[1] + 1] = self.map[check[0], self.robot[1]: check[1]]
            self.map[tuple(self.robot)] = 0
        
        else:
            seen = set() # vertical_to_move method will double count if vertical boxes
            
            # move all objects in backwards order (to prevent overwriting)
            for obj in self.vertical_to_move(self.robot, direction)[::-1]:
                if tuple(obj) in seen:
                    continue
                
                seen.add(tuple(obj))
        
                self.map[tuple(obj + direction)] = self.map[(tuple(obj))]
                self.map[(tuple(obj))] = 0
                
            # finally move the robot
            self.map[tuple(self.robot + direction)] = 3
            self.map[tuple(self.robot)] = 0
                
        self.robot += direction
        return True

def main(data: str) -> tuple[int]:
    wh, movements = data.split("\n\n")
    movements = np.array([{
        "^": UP,
        "v": DOWN,
        "<": LEFT,
        ">": RIGHT,    
    }[i] for i in list(movements.replace("\n", ""))])
    
    warehouse = Warehouse(wh)
    resized = WarehouseResized(wh)
    
    # Part 1 & 2
    for m in movements:
        warehouse.move(m)
        resized.move(m)

    return warehouse.gps_sum(), resized.gps_sum()

def main_animation(data: str): # to debug, hold down SPACE to fast forward, CAPSLOCK to increment step-by-step
    wh, movements = data.split("\n\n")
    movements = np.array([{
        "^": UP,
        "v": DOWN,
        "<": LEFT,
        ">": RIGHT,
    }[i] for i in list(movements.replace("\n", ""))])

    resized = WarehouseResized(wh)
    anim = WarehouseAnimation(resized, movements)
    anim.run()

if __name__ == "__main__":
    #main_animation(data)
    print(main(data))