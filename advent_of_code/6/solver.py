from math import prod

import advent


class Solver(advent.Advent):
    def process_data(self, data):
        split_points = [i - 1 for i, x in enumerate(data[-1]) if not x.isspace()]
        operators = data.pop().strip().split()
        numbers = [
            [line[l + 1 : r] for line in data]
            for l, r in zip(split_points, split_points[1:] + [len(data[0])])
        ]
        return numbers, operators

    def numbers_and_operator(self, numbers, operator):
        return sum(numbers) if operator == "+" else prod(numbers)

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
