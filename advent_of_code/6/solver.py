import advent


class Solver(advent.Advent):
    def process_data(self, data):
        return [data]

    def part_1(self, data):
        problems = list(zip(*(x.split() for x in data)))
        total = 0
        for problem in problems:
            numbers, operator = problem[:-1], problem[-1]
            if operator == "+":
                total += sum(int(x) for x in numbers)
            elif operator == "*":
                prod = 1
                for x in numbers:
                    prod *= int(x)
                total += prod
        return total

    def part_2(self, data):
        line_length = max(map(len, data))
        data = [x.ljust(line_length) for x in data]
        operator, numbers = "+", [0]
        total = 0
        for line in [[x.strip() for x in line] for line in zip(*data)] + [["+"]]:
            operator_candidate = line.pop()
            if operator_candidate:
                if operator == "+":
                    total += sum(numbers)
                elif operator == "*":
                    prod = 1
                    for x in numbers:
                        prod *= x
                    total += prod
                numbers = []
                operator = operator_candidate
            if any(line):
                numbers.append(int("".join(line).strip()))
        return total
