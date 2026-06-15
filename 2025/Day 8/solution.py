from AdventUtils import *

class Day8(Solution):
    def __init__(self, *, test_data: Optional[str] = None, memoization_type: Optional[type] = None) -> None:
        super().__init__(test_data=test_data, memoization_type=memoization_type)

    def parse_input(self, data: str) -> None:
        nodes = recursive_split(data.strip(), int, *"\n,")
        return nodes, sorted(it.combinations(nodes, 2), key = lambda x: np.linalg.norm(np.array(x[1]) - np.array(x[0])))

    def part_1(self, data: List[Any]) -> Union[int, str]: 
        nodes, pairs = data
        
        graph = Graph()
        
        for i in nodes:
            graph.add_node(tuple(i))
        
        add = 10 if self.use_test_data else 1000
        while pairs and add:
            p = pairs.pop(0)
            
            if not graph.add_edge(tuple(p[0]), tuple(p[1])):
                continue
            
            add -= 1
        
        return prod(sorted([len(component) for component in graph.get_connected_components()])[-3:])
    
    def part_2(self, data: List[Any]) -> Union[int, str]: 
        nodes, pairs = data

        uf = UnionFind([tuple(n) for n in nodes])
        
        for x, y in pairs:
            uf.union(tuple(x), tuple(y))
            
            if uf.sets == 1:
                return x[0] * y[0]
        
        return None

if __name__ == "__main__":
    solution = Day8(
        test_data = """162,817,812
57,618,57
906,360,560
592,479,940
352,342,300
466,668,158
542,29,236
431,825,988
739,650,466
52,470,668
216,146,977
819,987,18
117,168,530
805,96,715
346,949,466
970,615,88
941,993,340
862,61,35
984,92,344
425,690,689"""
    )

    print(solution.main(use_test_data=False))