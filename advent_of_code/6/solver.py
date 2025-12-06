from functools import reduce
from operator import add, mul

import advent


class Solver(advent.Advent):
    def process_data(self, data):
        operators = data.pop().strip().split()
        split_points = (
            [-1]
            + [
                i
                for i in range(len(data[0]))
                if all(line[i].isspace() for line in data)
            ]
            + [len(data[0])]
        )
        numbers = [
            [line[l + 1 : r] for line in data]
            for l, r in zip(split_points, split_points[1:])
        ]
        return numbers, operators

    def numbers_and_operator(self, numbers, operator):
        return reduce({"+": add, "*": mul}[operator], numbers)

    def part_1(self, numbers, operators):
        return sum(
            self.numbers_and_operator(map(int, num), op)
            for num, op in zip(numbers, operators)
        )

    def part_2(self, numbers, operators):
        return sum(
            self.numbers_and_operator(map(lambda x: int("".join(x)), zip(*num)), op)
            for num, op in zip(numbers, operators)
        )
