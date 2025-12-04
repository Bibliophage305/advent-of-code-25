import advent
from itertools import chain, accumulate


class Solver(advent.Advent):
    def process_data(self, data):
        return [
            [
                int(x.strip()[1:]) if x.strip()[0] == "R" else -int(x.strip()[1:])
                for x in data
            ]
        ]

    def zero_count(self, steps):
        return sum(x % 100 == 0 for x in accumulate(steps, initial=50))

    def part_1(self, steps):
        return self.zero_count(steps)

    def part_2(self, steps):
        return self.zero_count(
            chain.from_iterable([step // abs(step)] * abs(step) for step in steps)
        )
