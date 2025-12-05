import api


class Advent:

    test_data_paths = ["test_data", "test_data"]

    def __init__(self, day):
        self.day = day

    def process_data(self, data):
        return [data]

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
    
    def _get_test_solution(self, part):
        filename = f"advent_of_code/{self.day}/test_solution_{part}"
        try:
            with open(filename, "r") as f:
                content = f.read().strip()
                if not content:
                    raise ValueError(f"Test solution file {filename} is empty")
                return int(content)
        except FileNotFoundError as e:
            try:
                test_solution = api.get_test_solution(int(self.day), part)
                with open(filename, "w") as f:
                    f.write(str(test_solution))
                return int(test_solution)
            except Exception as e2:
                raise FileNotFoundError(
                    f"Test solution file {filename} doesn't exist and could not be retrieved from the API"
                ) from e2
        except ValueError as e:
            raise ValueError(f"Test solution in file {filename} is not a valid integer") from e

    def _run_test(self, part):
        f = getattr(self, f"part_{part}")
        expected_solution = self._get_test_solution(part)
        data = self._get_data(
            f"advent_of_code/{self.day}/{self.test_data_paths[part-1]}"
        )
        if not expected_solution:
            raise AssertionError(
                f"Test for part {part} failed\nExpected solution cannot be empty"
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
        data = self._get_data(f"advent_of_code/{self.day}/input_data")
        return getattr(self, f"part_{part}")(*data)

    def run(self):
        try:
            levels_solved = api.number_of_parts_solved(self.day)
            attempt_submit = True
        except Exception as e:
            attempt_submit = False

        for part in (1, 2):
            try:
                self._run_test(part)
            except AssertionError as e:
                print(e)
                return
            except Exception as e:
                raise Exception(f"Failed when running tests for part {part}") from e
            try:
                solution = self._run_solution(part)
                print(f"Part {part}: {solution}")
                if attempt_submit and levels_solved < part:
                    try:
                        api.submit_solution(self.day, part, solution)
                    except Exception as e:
                        raise Exception(
                            f"Could not submit solution for part {part}"
                        ) from e
            except Exception as e:
                raise Exception(f"Could not run part {part}") from e
