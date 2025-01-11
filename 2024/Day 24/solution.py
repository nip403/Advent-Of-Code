from AdventUtils import *

Char: TypeAlias = str
Gate: TypeAlias = str
T = TypeVar("T")
NestedList: TypeAlias = Union[T, List[T]]
ValidCircuit: TypeAlias = NestedList[Gate]
BitArray: TypeAlias = np.ndarray[bool]

class Circuit:
    gate_map = {
        "AND": "&",
        "OR": "|",
        "XOR": "^",
    }
    
    @staticmethod
    def backtrack_val(gate: Gate, wires: Mapping[Gate, bool], gates: list[list[Union[Gate, str]]]) -> bool:
        if gate in wires:
            return wires[gate]
        
        idx = np.where(gates[:, -1] == gate)[0][0]    
        a, op, b = gates[idx, :3]

        if op == "XOR":
            result = Circuit.backtrack_val(a, wires, gates) ^ Circuit.backtrack_val(b, wires, gates)

        elif op == "OR":
            result = Circuit.backtrack_val(a, wires, gates) | Circuit.backtrack_val(b, wires, gates)
            
        elif op == "AND":
            result = Circuit.backtrack_val(a, wires, gates) & Circuit.backtrack_val(b, wires, gates)

        wires[gate] = result
        return result    
    
    @staticmethod
    def build_circuit(gate: Gate, initial_wires: Mapping[Gate, bool], gates: list[list[Union[Gate, str]]]) -> NestedList[Gate]:        
        if gate in initial_wires or gate in "XOR AND OR".split():
            return gate
        
        return [Circuit.build_circuit(element, initial_wires, gates) for element in gates[gates[:, -1] == gate][0, :3]]

    @staticmethod
    def print_circuit(circuit: ValidCircuit) -> None:
        if isinstance(circuit, list):
            if len(circuit) == 3:
                left = Circuit.print_circuit(circuit[0])  
                right = Circuit.print_circuit(circuit[2]) 
                
                return f"{left} {Circuit.gate_map[circuit[1]]} {right}"
        else:
            return str(circuit)
        
        raise Exception(f"Invalid circuit passed: {circuit}")

class Day24(Solution):
    """
        __dict__:
            data
            test_data
            memo
    """
    
    def __init__(self, *, test_data: Optional[str] = None, memoization_type: Optional[type] = None) -> None:
        super().__init__(test_data=test_data, memoization_type=memoization_type)

    def parse_input(self, data: str) -> None:
        wires, gates = data.split("\n\n")

        return {
            "wires": {wire_id: int(val) for wire_id, val in [i.split(": ") for i in wires.splitlines()]}, 
            "gates": np.array([i.split() for i in gates.splitlines()])}
    
    def to_decimal(self, binary_arr: np.ndarray) -> int:
        return int(''.join(binary_arr.astype(int).astype(str)), 2)

    def adder(self, a: bool, b: bool) -> tuple[bool]:
        return a & b, a ^ b
    
    def ripple_carry_adder(self, a: BitArray, b: BitArray) -> BitArray:
        assert len(a) == len(b)
        
        result = np.zeros(len(a), dtype=bool)
        carry = False
        
        for i in range(len(a)):
            result[i] = a[i] ^ b[i] ^ carry
            carry = (a[i] & b[i]) | (b[i] & carry) | (a[i] & carry)
            
        return result if not carry else np.concatenate((result, np.array([True], dtype=bool)))
    
    def get_gate(self, letter: Char, number: int) -> Gate:
        return f"{letter}{"0" if number < 10 else ""}{number}"
    
    def build_z(self, z_gates: set[Gate], wires: Mapping[Gate, bool], gates: list[list[Union[Gate, str]]]) -> BitArray:        
        z_binary = np.empty(len(z_gates), dtype=bool)

        for gate in z_gates:
            z_binary[int(gate[1:])] = Circuit.backtrack_val(gate, wires, gates)
        
        return z_binary

    def part_1(self, data: List[Any]) -> Union[int, str]:
        wires = data["wires"]
        gates = data["gates"]
        
        self.all_z = set()
        
        for g in gates:
            if g[0].startswith("z"):
                self.all_z.add(g[0])
                
            if g[2].startswith("z"):
                self.all_z.add(g[4])  
            
            if g[4].startswith("z"):
                self.all_z.add(g[4])

        return self.to_decimal(self.build_z(self.all_z, copy.deepcopy(wires), gates)[::-1]) # [zn, z(n-1), z(n-2), ..., z02, z01, z00]
    
    def part_2(self, data: List[Any]) -> Union[int, str]: 
        gates = data["gates"]
        
        """ # just trying to get a visualisation (it didn't help at all)
        circuits: Mapping[Gate, NestedList[Gate]] = {}
        
        for i in range(len(self.all_z)):
            print(Circuit.print_circuit(Circuit.build_circuit(self.get_gate("z", i), data["wires"], gates))
        """
        
        """ 
        answer from a very helpful explanation from some very smart people: https://www.reddit.com/r/adventofcode/comments/1hla5ql/2024_day_24_part_2_a_guide_on_the_idea_behind_the/
        i assume this is all derived from ripple carry adder logic
        
        A gate is faulty if:
            1 - If the output of a gate is z, then the operation has to be XOR unless it is the last bit. 
            2 - If the output of a gate is not z and the inputs are not x, y then it has to be AND / OR, but not XOR. 
            3 - If you have a XOR gate with inputs x, y, there must be another XOR gate with this gate as an input. Search through all gates for an XOR-gate with this gate as an input; if it does not exist, your (original) XOR gate is faulty. These don't apply for the gates with input x00, y00.
            4 - If you have an AND-gate, there must be an OR-gate with this gate as an input. If that gate doesn't exist, the original AND gate is faulty. These don't apply for the gates with input x00, y00.
        """
        
        faulty = []
        all_XOR = gates[gates[:, 1] == "XOR"]
        all_OR = gates[gates[:, 1] == "OR"]
        
        for gate in gates:
            a, op, b, _, out = gate
             
            if (out.startswith("z") and not out == self.get_gate("z", len(self.all_z) - 1) and not op == "XOR") or \
                (not out.startswith("z") and not any(any(g.startswith(l) for l in "xy") for g in [a, b]) and op == "XOR") or \
                (not (a[-2:] == "00" or b[-2:] == "00") and all(any(g.startswith(l) for l in "xy") for g in [a, b]) and op == "XOR" and not out in np.ravel(all_XOR[:, [0, 2]])) or \
                (not (a[-2:] == "00" or b[-2:] == "00") and op == "AND" and not out in np.ravel(all_OR[:, [0, 2]])):
                faulty.append(gate)
        
        return ",".join(sorted(np.array(faulty)[:, -1], key=lambda x: (ord(x[0]), ord(x[1]), ord(x[2]))))

if __name__ == "__main__":
    solution = Day24()
    print(solution.main(use_test_data=False))