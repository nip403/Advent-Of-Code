import os

def getinput():
    with open(os.path.split(__file__)[0] + "\\input.txt", "r") as f:
        data = f.read().rstrip().split("\n\n")

    return data

""" IM STUPID AND BELOW IS BROKEN FOR ONE VALUE WHAT
def _parse(str_array):
    if not len(str_array):
        return 

    if not "[" in str_array:
        return int(str_array)

    # try to identify every element within outermost list
    str_array = str_array.replace(" ", "")
    outarr = []
    leftbracket = 0
    current = ""
    leftbracketinc = False

    for c in str_array[1:-1]:
        if c == "," and not leftbracket:
            outarr.append(_parse(current))
            current = ""
        else:
            current += c
    
            if c == "[":
                leftbracket += 1
                leftbracketinc = True
            elif c == "]":
                leftbracket -= 1
            
            continue
        
    outarr.append([] if len(current) == 2 else _parse(current))

    return outarr

def _remove_none(arr):
    if None in arr:
        return []
    
    out = []
    for i in arr:
        if isinstance(i, list):
            out.append(_remove_none(i))
        else:
            out.append(i)

    return out
"""

def parse_packets(raw):
    return [list(map(eval, pair.split("\n"))) for pair in raw]

    # bruh why didnt i realise eval was a thing
    """
    packets = []

    for pair in raw:
        outpair = [_parse(i) for i in pair.split("\n")]
        packets.append(_remove_none(outpair))

    return packets
    """

def compare(left, right):
    #print("Compare", left, right)

    if isinstance(left, int) and isinstance(right, int):
        if left == right:
            return None # signal to continue

        return left < right

    if isinstance(left, int) and isinstance(right, list):
        left = [left]
    
    if isinstance(left, list) and isinstance(right, int):
        right = [right]

    # at this point both are lists
    i = 0

    while i < len(left) and i < len(right):
        result = compare(left[i], right[i])

        if result is not None: # if there is definitive result
            return result 

        i += 1

    if i == len(left):
        if len(left) == len(right): # both ended same time with no definite result, need to continue
            return None
        
        return True # left ended before right

    if i == len(right): # right ended before left
        return False

def part1():
    packets = parse_packets(getinput())
    total = 0

    for n, pair in enumerate(packets):
        left, right = pair 

        #print(n+1, end=" ")
        if compare(left, right): 
            #print(True)
            total += n + 1
        else:
            #print(False)
            pass

    return total

def partition(arr, low, high):
    pivot = arr[high]
    i = low - 1

    for j in range(low, high):
        if compare(arr[j], pivot):
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    
    i += 1
    arr[i], arr[high] = arr[high], arr[i]

    return arr, i

def quicksort(arr, low, high): # using key compare
    if low >= high or low < 0:
        return
    
    arr, p = partition(arr, low, high)
    quicksort(arr, low, p - 1)
    quicksort(arr, p + 1, high)

    return arr

def part2():
    data = parse_packets(getinput())
    packets = []
    divider = [[[2]], [[6]]]

    for i in data:
        for j in range(2):
            packets.append(i[j])
    
    packets += [[[2]], [[6]]]
    packets = quicksort(packets, 0, len(packets) - 1)
    
    decoder = 1

    for row, packet in enumerate(packets):
        if packet in divider:
            decoder *= row + 1
    
    return decoder
    
if __name__ == "__main__":
    print("Part 1:", part1()) 
    print("Part 2:", part2())
