from itertools import product
from advent_of_code import advent


class Solver(advent.Advent):
    part_1_test_solution = 13
    part_2_test_solution = 43

    def process_data(self, data):
        return [[x.strip() for x in data]]
    
    def can_remove(self, data):
        ats = {p for p in product(range(len(data)), range(len(data[0]))) if data[p[0]][p[1]] == "@"}
        ret = set()
        for row_index, col_index in ats:
            adjacent_positions = set(product(
                range(row_index - 1, row_index + 2),
                range(col_index - 1, col_index + 2),
            ))
            if len(ats & adjacent_positions) < 5:
                ret.add((row_index, col_index))
        return ret

    def part_1(self, data):
        return len(self.can_remove(data))

    def part_2(self, data):
        total = 0
        while True:
            removable = self.can_remove(data)
            if not removable:
                return total
            total += len(removable)
            data = [
                "".join(
                    "." if (row_index, col_index) in removable else cell
                    for col_index, cell in enumerate(row)
                )
                for row_index, row in enumerate(data)
            ]
