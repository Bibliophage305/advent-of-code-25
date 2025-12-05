from itertools import accumulate, chain

import advent


class Solver(advent.Advent):
    def process_data(self, data):
        return [[int(x[1:]) if x[0] == "R" else -int(x[1:]) for x in data]]

    def zero_count(self, steps):
        return sum(x % 100 == 0 for x in accumulate(steps, initial=50))

    def part_1(self, steps):
        return self.zero_count(steps)

    def part_2(self, steps):
        return self.zero_count(
            chain.from_iterable([step // abs(step)] * abs(step) for step in steps)
        )
