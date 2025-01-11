import os

def getinput():
    with open(os.path.split(__file__)[0] + "\\input.txt", "r") as f:
        data = f.read().rstrip().split("\n\n")

    return data

class Monkey:
    def __init__(self, notes):
        lines = [i.replace(" ", "") for i in notes.split("\n")]

        self.number = lines[0][-2]

        # 1st line with items
        self.items = list(map(int, lines[1].split(":")[-1].split(",")))

        # 2nd line with worry after inspection
        self.worry_operation = lines[2].split("=")[-1] # stored as string to pass to exec()

        # 3rd line test to decide where item goes
        self.test_div = int(lines[3].split("by")[-1])

        # 4th line true condition
        self.test_true = int(lines[4].split("monkey")[-1])

        # 5th line false condition
        self.test_false = int(lines[5].split("monkey")[-1])

        self.inspections = 0

    def setup_part2(self):
        self.items = [list(i) for i in self.items]

    def __repr__(self):
#        return f"""Items: {self.items}
#    Op: {self.worry_operation}
#    Test: div by {self.test_div}
#        True:  To monkey {self.test_true}
#        False: To monkey {self.test_false}
#"""
        return f"Monkey {self.number}: {self.items}"

    def turn(self, monkeys):
        for old in self.items:
            new = eval(self.worry_operation) // 3

            self.inspections += 1

            if not new % self.test_div: # divisible
                monkeys[self.test_true].items.append(new)
            else:
                monkeys[self.test_false].items.append(new)

        self.items = []

        return monkeys

    def turn_2(self, monkeys):
        mod = 1
        for m in monkeys:
            mod *= m.test_div

        for old in self.items:
            # can modulo the massive worry factors with total modulo of all monkeys as result of monkeys throwing only depends on divisibility after operation
            new = eval(self.worry_operation)
            self.inspections += 1
            new %= mod

            if not new % self.test_div: # divisible
                monkeys[self.test_true].items.append(new)
            else:
                monkeys[self.test_false].items.append(new)

        self.items = []

        return monkeys

def part1(rounds=20):
    data = getinput()
    monkeys = [Monkey(m) for m in data]
    groupsize = len(monkeys)
    rounds_elapsed = 0

    for r in range(rounds):
        for current in range(len(monkeys)):
            monkeys = monkeys[current].turn(monkeys)

    inspection_count = sorted([m.inspections for m in monkeys])

    return inspection_count[-1] * inspection_count[-2]

def part2(rounds=10000):
    data = getinput()
    monkeys = [Monkey(m) for m in data]
    groupsize = len(monkeys)
    rounds_elapsed = 0

    for r in range(rounds):
        for current in range(len(monkeys)):
            monkeys = monkeys[current].turn_2(monkeys)

    inspection_count = sorted([m.inspections for m in monkeys])

    return inspection_count[-1] * inspection_count[-2]

if __name__ == "__main__":
    print("Part 1:", part1())
    print("Part 2:", part2())
