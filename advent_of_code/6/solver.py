from functools import reduce
from operator import mul

import advent


class Solver(advent.Advent):
    def process_data(self, data):
        return [data]

    def numbers_and_operator(self, numbers, operator):
        return sum(numbers) if operator == "+" else reduce(mul, numbers, 1)

    def part_1(self, data):
        problems = list(zip(*(x.split() for x in data)))
        return sum(
            self.numbers_and_operator(map(int, problem[:-1]), problem[-1])
            for problem in problems
        )

    def part_2(self, data):
        numbers, operators = [], []
        for line in [[x.strip() for x in line] for line in zip(*data)]:
            operator_candidate = line.pop()
            if operator_candidate:
                operators.append(operator_candidate)
                numbers.append([])
            if any(line):
                numbers[-1].append(int("".join(line).strip()))
        return sum(
            self.numbers_and_operator(nums, op) for nums, op in zip(numbers, operators)
        )
