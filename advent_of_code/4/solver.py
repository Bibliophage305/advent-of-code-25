from itertools import product
import advent


class Solver(advent.Advent):
    def process_data(self, data):
        return [{p for p in product(range(len(data)), range(len(data[0].strip()))) if data[p[0]][p[1]] == "@"}]
    
    def can_remove(self, data):
        ret = set()
        for row_index, col_index in data:
            adjacent_positions = set(product(
                range(row_index - 1, row_index + 2),
                range(col_index - 1, col_index + 2),
            ))
            if len(data & adjacent_positions) < 5:
                ret.add((row_index, col_index))
        return ret

    def part_1(self, data):
        return len(self.can_remove(data))

    def part_2(self, data):
        total = 0
        while removable := self.can_remove(data):
            total += len(removable)
            data = data - removable
        return total
