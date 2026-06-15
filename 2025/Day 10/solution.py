from AdventUtils import *

class Day10(Solution):
    """
        __dict__:
            data
            test_data
            memo
    """

    def __init__(self, *, test_data: Optional[str] = None, memoization_type: Optional[type] = None) -> None:
        super().__init__(test_data=test_data, memoization_type=memoization_type)

    def parse_input(self, data: str) -> None:
        data = string_multi_replace(data.strip(), "(){}[]").split("\n")
        return recursive_split(data, lambda x: int(x) if x.isdigit() else x, *" ,")

    def part_1(self, data: List[Any]) -> Union[int, str]: 
        presses = 0
        
        # how dare my linear algebra course come in useful
        for machine in data[:]:
            target = np.array(list(machine[0][0].replace(".", "0").replace("#", "1")), dtype=int)
            *switches, _ = machine[1:]
            
            # build augmented matrix
            coeff_mat = np.zeros((target.shape[0], len(switches)), dtype=int)
            
            for i, s in enumerate(switches):
                coeff_mat[s, i] = 1
                
            rref = rref_gf2(np.c_[coeff_mat, target])
            
            """
            particular = rref[:, -1]
            pivots, free = find_pivots(rref)
            basis_vectors = coeff_mat.T[free]
            """
            pivots, free = find_pivots(rref)
            num_switches = len(switches)

            particular = np.zeros(num_switches, dtype=int)
            for r, c in enumerate(pivots):
                particular[c] = rref[r, -1]
                
            # if the free switch i pressed, which pivot switches must also be pressed so that nothing happens to the lights
            null_space = np.zeros((len(switches), len(free)), dtype=int)
            
            for i, f_idx in enumerate(free):
                null_space[f_idx, i] = 1
            
            rref_free_block = rref[:len(pivots), free]
            
            for i, p_idx in enumerate(pivots):
                null_space[p_idx, :] = rref_free_block[i, :]

            basis_vectors = list(null_space.T)

            xor = lambda part, bases: part if not bases else xor(part ^ bases[0], bases[1:])
            powerset = [c for v in range(len(basis_vectors) + 1) for c in combinations(basis_vectors, v)]
            presses += min(sum(xor(particular, bases)) for bases in powerset)
        
        return presses
    
    def part_2(self, data: List[Any]) -> Union[int, str]: 
        presses = 0
    
        for machine in data:
            *switches, joltage = machine[1:]
            
            # build augmented matrix
            coeff_mat = np.zeros((len(joltage), len(switches)), dtype=int)
            
            for i, s in enumerate(switches):
                coeff_mat[s, i] = 1
                
            
            res = scipy.optimize.milp(
                np.ones(coeff_mat.shape[1]),
                integrality=np.ones(coeff_mat.shape[1]),
                constraints=scipy.optimize.LinearConstraint(coeff_mat, joltage, joltage),
            )
            
            presses += res.fun
            
        return int(presses)

if __name__ == "__main__":
    solution = Day10(
        test_data = """[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}"""
    )

    print(solution.main(use_test_data=False))