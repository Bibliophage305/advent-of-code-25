import advent


class Solver(advent.Advent):
    def process_data(self, data):
        ranges, ingredients = [], []
        in_ranges = True
        for line in data:
            if not line:
                in_ranges = False
                continue
            if in_ranges:
                ranges.append(list(map(int, line.split("-"))))
            else:
                ingredients.append(int(line))
        ranges.sort()
        merged_ranges = []
        for start, end in ranges:
            if not merged_ranges or merged_ranges[-1][1] < start - 1:
                merged_ranges.append([start, end])
            else:
                merged_ranges[-1][1] = max(merged_ranges[-1][1], end)
        return merged_ranges, ingredients

    def part_1(self, ranges, ingredients):
        return sum(
            any(start <= ingredient <= end for start, end in ranges)
            for ingredient in ingredients
        )

    def part_2(self, ranges, ingredients):
        return sum(1 + end - start for start, end in ranges)
