from functools import cache

import advent


class Solver(advent.Advent):
    def process_data(self, data):
        return [[list(map(int, s.split("-"))) for s in "".join(data).split(",")]]

    def count_bad_ids(self, data, min_chunk_size):
        @cache
        def valid_chunk_sizes(l):
            return [
                size for size in range(min_chunk_size(l), l // 2 + 1) if l % size == 0
            ]

        total = 0
        for start, end in data:
            for i in range(start, end + 1):
                s = str(i)
                l = len(s)
                for chunk_size in valid_chunk_sizes(l):
                    first_chunk = s[:chunk_size]
                    for j in range(chunk_size, l, chunk_size):
                        if s[j : j + chunk_size] != first_chunk:
                            break
                    else:
                        total += i
                        break
        return total

    def part_1(self, data):
        return self.count_bad_ids(data, lambda l: (l + 1) // 2)

    def part_2(self, data):
        return self.count_bad_ids(data, lambda _: 1)
