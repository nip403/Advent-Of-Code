from AdventUtils import *

class Day11(Solution):
    """
        __dict__:
            data
            test_data
            memo
    """

    def __init__(self, *, test_data: Optional[str] = None, memoization_type: Optional[type] = None) -> None:
        super().__init__(test_data=test_data, memoization_type=memoization_type)

    def parse_input(self, data: str) -> None:
        return recursive_split(data, None, "\n", ": ")

    def part_1(self, data: List[Any]) -> Union[int, str]: 
        dg = DirectedGraph()
        
        for a, b in data:
            for i in b.split():
                dg.add_edge(a, i)
            
        return len(dg.get_paths("you", "out"))
    
    def part_2(self, data: List[Any]) -> Union[int, str]: 
        dg = DirectedGraph()
        
        for a, b in data:
            for i in b.split():
                dg.add_edge(a, i)
        
        # pretty happy with the idea
        svr_dac = dg.count_paths("svr", "dac", avoid={"out", "fft"})
        svr_fft = dg.count_paths("svr", "fft", avoid={"out", "dac"})
        dac_fft = dg.count_paths("dac", "fft", avoid={"out", "svr"})
        fft_dac = dg.count_paths("fft", "dac", avoid={"out", "svr"})
        dac_out = dg.count_paths("dac", "out", avoid={"fft", "svr"})
        fft_out = dg.count_paths("fft", "out", avoid={"dac", "svr"})
        
        return (svr_dac * dac_fft * fft_out) + (svr_fft * fft_dac * dac_out) 

if __name__ == "__main__":
    solution = Day11(
        test_data = """aaa: you hhh
you: bbb ccc
bbb: ddd eee
ccc: ddd eee fff
ddd: ggg
eee: out
fff: out
ggg: out
hhh: ccc fff iii
iii: out"""
    )

    print(solution.main(use_test_data=False))