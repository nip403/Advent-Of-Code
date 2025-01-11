import os

def getinput():
    with open(os.path.split(__file__)[0] + "\\input.txt", "r") as f:
        data = f.read().rstrip().split("\n")

    return data

def parse_data(data):
    coords = []

    for d in data:
        sensor, beacon = d.split(": ")
        sensor = [int(sensor.split("=")[-2].split(",")[0]), int(sensor.split("=")[-1])]
        beacon = [int(beacon.split("=")[-2].split(",")[0]), int(beacon.split("=")[-1])]

        coords.append(
            [
                sensor,
                manhattan(sensor, beacon),
            ]
        )

    return coords

def manhattan(x, y):
    return abs(x[0] - y[0]) + abs(x[1] - y[1])

def get_boundaries(coords, y):
    # compute greatest and least possible x value that is not possible on y=2million
    lowest, highest = None, None
    relevant = []

    for p, c in enumerate(coords):
        sensor, dist = c
        y_dist = abs(y - sensor[1])

        # check if range reaches y level, if not break and discard
        if y_dist > dist:
            continue

        remaining = dist - y_dist   

        # check least x and overwrite
        least_x = sensor[0] - remaining

        if lowest is None or least_x < lowest:
            lowest = least_x

        # check greatest x and overwrite
        most_x = sensor[0] + remaining

        if highest is None or most_x > highest:
            highest = most_x
        
        relevant.append(p)

    # return lowest, highest, relevant coords (i.e. if coords does not affect y=2mil, discard)
    return lowest, highest, [i for p, i in enumerate(coords) if p in relevant]

def part1():
    coords = parse_data(getinput())
    y = 2_000_000
    xmin, xmax, coords = get_boundaries(coords, y)
    not_present = []

    for x in range(xmin, xmax): # idk thought it was xmax + 1 but i guess not
        for sensor, dist in coords:
            if manhattan(sensor, [x, y]) <= dist:
                not_present.append(x)
                break

    return len(not_present)

class Region:
    def __init__(self, xy, dist):
        self.x = xy[0]
        self.y = xy[1]
        self.d = dist

    def __repr__(self):
        return f"({self.x}, {self.y}), dist={self.d}"

    def lines(self):
        # y intercepts
        self.intercepts_neg_gradient = []
        self.intercepts_pos_gradient = []
        
        top = [self.x, self.y - self.d]
        bottom = [self.x, self.y + self.d]

        # lines sloping down
        self.intercepts_neg_gradient.append(sum(top))
        self.intercepts_neg_gradient.append(sum(bottom))

        # sloping up
        self.intercepts_pos_gradient.append(top[1] - top[0])
        self.intercepts_pos_gradient.append(bottom[1] - bottom[0])

def get_regions(coords):
    return [Region(*c) for c in coords]

def part2():
    coords = parse_data(getinput())
    
    # only 1 possible beacon, therefore ALL 4 sides of beacon must touch exclusion regions
    # so need to find 2 pairs of regions dist 1 apart

    regions = get_regions(coords)
    all_pos = []
    all_neg = []

    for r in regions:
        r.lines()

        all_pos += r.intercepts_pos_gradient
        all_neg += r.intercepts_neg_gradient

    # for lines find 2 lines 2 units intercept apart
    for i in range(len(all_pos)):
        for j in range(i + 1, len(all_pos)):
            pos_a = all_pos[i]
            pos_b = all_pos[j]
            neg_a = all_neg[i]
            neg_b = all_neg[j]

            if abs(pos_a - pos_b) == 2: 
                pos_middle = (pos_a + pos_b) // 2

            if abs(neg_a - neg_b) == 2: 
                neg_middle = (neg_a + neg_b) // 2

    # now we have coords of intercepts between the 2 pairs of lines, just need to extend lines
    """
    for intercept: positive line = negative line so:
    x + pos_middle = -x + neg_middle
    2x = neg_middle - pos_middle
    x = (neg_middle - pos_middle) // 2
    y = x + pos_middle
    """

    x = (neg_middle - pos_middle) // 2
    y = x + pos_middle

    return (x * 4000000) + y, x, y
    
if __name__ == "__main__":
    print("Part 1:", part1())
    print("Part 2:", part2())