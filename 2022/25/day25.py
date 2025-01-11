import os

def getinput():
    with open(os.path.split(__file__)[0] + "\\input.txt", "r") as f:
        data = f.read().rstrip().split("\n")

    return data

ToDec = {
    "2": 2,
    "1": 1,
    "0": 0,
    "-": -1,
    "=": -2,
}

def to_decimal(snafu):
    num = 0
    exp = 0

    for i in snafu[::-1]:
        num += ToDec[i] * (5 ** exp)
        exp += 1

    return num

"""
last digit | snafu last digit

1 1
2 2
3 = (add 1 unit in next column)
4 -
5 0
"""

ToSNAFU = {
    1: "1",
    2: "2",
    3: "=",
    4: "-",
    0: "0",
}

def to_SNAFU(num):
    # units
    snafu = ToSNAFU[num % 5]

    # fives
    if num >= 3:
        fives = ((num - 3) // 5) + 1
        snafu = to_SNAFU(fives) + snafu

    return snafu

def part1():
    data = getinput()
    fuel_dec = sum(to_decimal(i) for i in data)

    return to_SNAFU(fuel_dec)

def part2():
    data = getinput()
    return
    
if __name__ == "__main__":
    print("Part 1:", part1())
    print("Part 2:", part2())