from advent_of_code import advent
from itertools import chain


class Solver(advent.Advent):
    part_1_test_solution = 3
    part_2_test_solution = 6

    def process_data(self, data):
        return [[int(x.strip()[1:]) if x.strip()[0] == "R" else -int(x.strip()[1:]) for x in data]]
    
    def zero_count(self, steps):
        position, zero_count = 50, 0
        for step in steps:
            position += step
            if position % 100 == 0:
                zero_count += 1
        return zero_count

    def part_1(self, steps):
        return self.zero_count(steps)

    def part_2(self, steps):
        return self.zero_count(chain.from_iterable((step // abs(step) for _ in range(abs(step))) for step in steps))
