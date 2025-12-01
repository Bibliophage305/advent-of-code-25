class Advent:

    test_data_paths = ["test", "test"]

    def __init__(self, day):
        self.day = day

    def process_data(self, data):
        return [data]

    def part_1_test_solution(self):
        raise ValueError

    def part_2_test_solution(self):
        raise ValueError

    def part_1(self, *data):
        raise NotImplementedError

    def part_2(self, *data):
        raise NotImplementedError

    def _read_data(self, filename):
        with open(filename, "r") as f:
            return f.readlines()

    def _get_data(self, filename):
        try:
            data = self._read_data(filename)
        except FileNotFoundError as e:
            raise FileNotFoundError(f"The file {filename} doesn't exist") from e
        return self.process_data(data)

    def _run_test(self, part):
        f = getattr(self, f'part_{part}')
        expected_solution = getattr(self, f'part_{part}_test_solution')
        data = self._get_data(
            f"advent_of_code/{self.day}/{self.test_data_paths[part-1]}"
        )
        if expected_solution is None:
            raise AssertionError(
                f"Test for part {part} failed\nExpected solution cannot be None"
            )
        try:
            solution = f(*data)
        except NotImplementedError as e:
            raise NotImplementedError(
                f"Solution function for part {part} is not implemented"
            ) from e
        if solution is None:
            raise AssertionError(
                f"Test for part {part} failed\nAnswer returned None, is the function implemented?"
            )
        if solution != expected_solution:
            raise AssertionError(
                f"Test for part {part} failed\nExpected {expected_solution}, got {solution}"
            )

    def _run_solution(self, part):
        data = self._get_data(f"advent_of_code/{self.day}/input")
        print(f"Part {part}: {getattr(self, f'part_{part}')(*data)}")


    def run(self):
        for part in (1, 2):
            try:
                self._run_test(part)
            except AssertionError as e:
                print(e)
                return
            except Exception as e:
                raise Exception(f"Failed when running tests for part {part}") from e
            try:
                self._run_solution(part)
            except Exception as e:
                raise Exception(f"Could not run part {part}") from e
