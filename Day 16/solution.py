from pathlib import Path
import heapq
import numpy as np

np.set_printoptions(threshold=np.inf, suppress=True, linewidth=np.inf)

with open(Path(__file__).parent / "input_data.txt", "r") as f:
    data = f.read()
    
UP = [-1, 0]
DOWN = [1, 0]
LEFT = [0, -1]
RIGHT = [0, 1]

DIRECTIONS = [UP, DOWN, LEFT, RIGHT]

def dijkstra(maze: np.ndarray, start: np.ndarray, end: np.ndarray) -> np.ndarray: # wow this is fast
    scores = np.full(tuple([*maze.shape, 4]), fill_value=np.iinfo(np.int32).max, dtype=int) # [y, x, direction when reaching]
    scores[*start] = 0
    
    pq = []
    heapq.heappush(pq, (0, *start, 3))
    
    while pq:
        score, y, x, direction = heapq.heappop(pq)

        if score > scores[y, x, direction]:
            continue
        
        for i, (dy, dx) in enumerate(DIRECTIONS):  
            ny, nx = y + dy, x + dx         
             
            if not (0 <= ny < maze.shape[0] and 0 <= nx < maze.shape[1]) or (maze[ny, nx] == -1): # OOB or wall
                continue
            
            add = 1 + (int(i != direction) * 1000) # score cost when moving from one node to another 
            
            if score + add < scores[ny, nx, i]: # push new candidate
                scores[ny, nx, i] = score + add
                heapq.heappush(pq, (score + add, ny, nx, i))
                
    return scores

def backtrack(maze: np.ndarray, scores: np.ndarray, start: np.ndarray, end: np.ndarray) -> set[tuple]: 
    best = set()
    final = np.min(scores[*end])
    stack = [(tuple(end), final, np.where(scores == final)[-1][0])] # [2]: direction of "path traverser" when reaching end with minimum score

    while stack:
        (y, x), score, direction = stack.pop()
        best.add((y, x))
        
        if np.all((y, x) == start):
            continue
        
        for (dy, dx) in DIRECTIONS:
            ny, nx = y + dy, x + dx
            
            if not (0 <= ny < scores.shape[0] and 0 <= nx < scores.shape[1]) or (maze[ny, nx] == -1):
                continue
    
            for d, n_score in enumerate(scores[ny, nx]):           
                add = 1 + (int(d != direction) * 1000) 
            
                if score - add == n_score:
                    stack.append(((ny, nx), n_score, d))
    
    return best

def main(data: str) -> tuple[int]:
    maze = np.array([[{
        "#": -1,
        ".": 0,
        "S": 1,
        "E": 2,
    }[j] for j in list(i)] for i in data.splitlines()])
    
    start = np.ravel(np.where(maze == 1))
    end = np.ravel(np.where(maze == 2))
    
    scores = dijkstra(maze, start, end)

    return int(np.min(scores[*end])), len(backtrack(maze, scores, start, end))

if __name__ == "__main__":
    print(main(data))