from pathlib import Path
from functools import cmp_to_key

with open(Path(__file__).parent / "input_data.txt", "r") as f:
    data = f.read()

def main(data: str) -> list[int]:
    rules, updates = data.split("\n\n")
    rules = [[int(i) for i in r.split("|")] for r in rules.split("\n")]
    updates = [[int(i) for i in u.split(",")] for u in updates.split("\n")]
    
    middle_sum = 0 # part 1
    corrected_middles = 0 # part 2
    
    # create better rule mapping
    rulebook = {}
    
    for r in rules:
        if r[0] in rulebook.keys():
            rulebook[r[0]].add(r[1])
        else:
            rulebook[r[0]] = set([r[1]])
            
    # some quicksort shenanigans
    def cmp(a: int, b: int) -> bool: # is a < b?
        return b in rulebook[a] # some space for error if neither are defined in rulebook, i have complete faith in the test dataset
        
    def partition(arr: list[int], low: int, high: int) -> int:
        pivot = arr[high]
        i = low
        
        for j in range(low, high):
            if cmp(arr[j], pivot):
                arr[i], arr[j] = arr[j], arr[i]
                i += 1
                
        arr[i], arr[high] = arr[high], arr[i]
        return i
            
    def sort_by_rules(arr: list[int], low: int, high: int) -> list[int]:
        if low >= high or low < 0:
            return arr
        
        p = partition(arr, low, high)
        
        sort_by_rules(arr, low, p - 1)
        sort_by_rules(arr, p + 1, high)
        
    for update in updates:
        for p, x in enumerate(update[1:], start=1):
            y = set(update[:p])
            
            if y & rulebook[x]: # if any of the numbers before each item in the update violates any rule (intersection with a rule going in the "opposite direction")
                break
            
        else: # part 1: update is correct
            middle_sum += update[len(update) // 2]
            continue
        
        # part 2: update is incorrect
        sort_by_rules(update, 0, len(update) - 1)
        corrected_middles += update[len(update) // 2]
            
    return middle_sum, corrected_middles

if __name__ == "__main__":
    print(main(data))