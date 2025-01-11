from AdventUtils import *

def backtrack_val(val: str, wires: dict[str, int], gates: list[list[str]]) -> bool:
    if val in wires:
        return wires[val]
    
    idx = np.where(gates[:, -1] == val)[0][0]    
    a, op, b = gates[idx, :3]

    if op == "XOR":
        result = backtrack_val(a, wires, gates) ^ backtrack_val(b, wires, gates)

    elif op == "OR":
        result = backtrack_val(a, wires, gates) | backtrack_val(b, wires, gates)
        
    elif op == "AND":
        result = backtrack_val(a, wires, gates) & backtrack_val(b, wires, gates)

    wires[val] = result
    return result    

class Day24(Solution):
    """
        __dict__:
            data
            test_data
            memo
    """
    def __init__(self, *, test_data: Optional[str] = None, memoization_type: Optional[type] = None) -> None:
        super().__init__(test_data=test_data, memoization_type=memoization_type)

    def process_data(self, data: str) -> None:
        wires, gates = data.split("\n\n")

        return {
            "wires": {wire_id: int(val) for wire_id, val in [i.split(": ") for i in wires.splitlines()]}, 
            "gates": np.array([i.split() for i in gates.splitlines()])}
    
    def to_decimal(self, binary_arr: np.ndarray) -> int:
        return int(''.join(binary_arr.astype(int).astype(str)), 2)

    def adder(self, a: bool, b: bool) -> tuple[bool]:
        return a & b, a ^ b

    def part_1(self, use_test_data: bool = False) -> Union[int, str]:
        data = self.data if not use_test_data else self.test_data
        wires = data["wires"]
        gates = data["gates"]
        
        all_z = set()
        
        for g in gates:
            if g[0].startswith("z"):
                all_z.add(g[0])
                
            if g[2].startswith("z"):
                all_z.add(g[4])  
            
            if g[4].startswith("z"):
                all_z.add(g[4])
                
        self.z_binary = np.empty(len(all_z), dtype=bool)

        for wire in all_z:
            self.z_binary[int(wire[1:])] = backtrack_val(wire, wires, gates)

        return self.to_decimal(self.z_binary[::-1])
    
    def part_2(self, use_test_data: bool = False) -> Union[int, str]:
        data = self.data if not use_test_data else self.test_data
        wires = data["wires"]
        gates = data["gates"]
        
        x = np.array([wires.get(f"x{"0" if i < 10 else ""}{i}", 0) for i in range(self.z_binary.size)], dtype=bool)[::-1]
        y = np.array([wires.get(f"y{"0" if i < 10 else ""}{i}", 0) for i in range(self.z_binary.size)], dtype=bool)[::-1]
        
        for i in reversed(range(x.size)): # work from smallest up
            carry, unit = self.adder(x[i], y[i])
            
            if not self.z_binary[i] == x[i] ^ y[i]:
                pass
        
        return

if __name__ == "__main__":
    dasta = """x00: 1
x01: 0
x02: 1
x03: 1
x04: 0
y00: 1
y01: 1
y02: 1
y03: 1
y04: 1

ntg XOR fgs -> mjb
y02 OR x01 -> tnw
kwq OR kpj -> z05
x00 OR x03 -> fst
tgd XOR rvg -> z01
vdt OR tnw -> bfw
bfw AND frj -> z10
ffh OR nrd -> bqk
y00 AND y03 -> djm
y03 OR y00 -> psh
bqk OR frj -> z08
tnw OR fst -> frj
gnj AND tgd -> z11
bfw XOR mjb -> z00
x03 OR x00 -> vdt
gnj AND wpb -> z02
x04 AND y00 -> kjc
djm OR pbm -> qhw
nrd AND vdt -> hwm
kjc AND fst -> rvg
y04 OR y02 -> fgs
y01 AND x02 -> pbm
ntg OR kjc -> kwq
psh XOR fgs -> tgd
qhw XOR tgd -> z09
pbm OR djm -> kpj
x03 XOR y03 -> ffh
x00 XOR y04 -> ntg
bfw OR bqk -> z06
nrd XOR fgs -> wpb
frj XOR qhw -> z04
bqk OR frj -> z07
y03 OR x01 -> nrd
hwm AND bqk -> z03
tgd XOR rvg -> z12
tnw OR pbm -> gnj"""

    data="""x00: 0
x01: 1
x02: 0
x03: 1
x04: 0
x05: 1
y00: 0
y01: 0
y02: 1
y03: 1
y04: 0
y05: 1

x00 AND y00 -> z05
x01 AND y01 -> z02
x02 AND y02 -> z01
x03 AND y03 -> z03
x04 AND y04 -> z04
x05 AND y05 -> z00"""
    
    solution = Day24(
        test_data = data
    )

    print(solution.main(use_test_data=False))