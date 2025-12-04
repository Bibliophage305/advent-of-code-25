import advent


class Solver(advent.Advent):
    def process_data(self, data):
        return [[x.strip() for x in data]]

    def largest_after_deletions(self, s, l):
        while len(s) > l:
            s = max(s[:i] + s[i + 1 :] for i in range(len(s)))
        return int(s)

    def part_1(self, data):
        return sum(self.largest_after_deletions(x, 2) for x in data)

    def part_2(self, data):
        return sum(self.largest_after_deletions(x, 12) for x in data)
