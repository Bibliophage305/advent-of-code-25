from advent_of_code import advent


class Solver(advent.Advent):
    part_1_test_solution = 1227775554
    part_2_test_solution = 4174379265

    def process_data(self, data):
        return [[list(map(int, s.split("-"))) for s in "".join(x.strip() for x in data).split(",")]]
    
    def count_bad_ids(self, data, min_chunk_size):
        total = 0
        for start, end in data:
            for i in range(start, end + 1):
                s = str(i)
                l = len(s)
                for chunk_size in range(min_chunk_size(l), l // 2 + 1):
                    if l % chunk_size != 0:
                        continue
                    chunks = {
                        s[j : j + chunk_size] for j in range(0, l, chunk_size)
                    }
                    if len(chunks) == 1:
                        total += i
                        break
        return total

    def part_1(self, data):
        total = 0
        for start, end in data:
            for i in range(start, end + 1):
                s = str(i)
                l = len(s)
                if l % 2 != 0:
                    continue
                if s[: l // 2] == s[l // 2 :]:
                    total += i
        return total

    def part_2(self, data):
        min_chunk_size = lambda x: 1
        return self.count_bad_ids(data, min_chunk_size)
