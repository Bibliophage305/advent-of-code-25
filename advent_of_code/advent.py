from pathlib import Path

import api


class Advent:
    """
    Base class for Advent of Code solution runners.

    Subclass this for each day. Implement:
        - process_data(self, raw_lines)
        - part_1(self, *data)
        - part_2(self, *data)
    """

    test_data_paths = ("test_data", "test_data")

    def __init__(self, day: int):
        self.day = int(day)
        self.base_path = Path("advent_of_code") / str(self.day)

    # ----------------------------------------------------------------------
    # Data helpers
    # ----------------------------------------------------------------------

    def process_data(self, lines: list[str]):
        """Override in subclasses. Default: return a single argument = raw line list."""
        return [lines]

    def _read_lines(self, filename: str) -> list[str]:
        path = self.base_path / filename
        try:
            return path.read_text().splitlines()
        except FileNotFoundError as exc:
            raise FileNotFoundError(f"Missing required file: {path}") from exc

    def _write_text(self, filename: str, content: str) -> None:
        (self.base_path / filename).write_text(content)

    def _load_data(self, filename: str):
        return self.process_data(self._read_lines(filename))

    # Generic pattern: load local file or fetch via API
    def _load_or_fetch(self, filename: str, fetch_fn, *, description: str):
        try:
            return self._read_lines(filename)
        except FileNotFoundError:
            pass

        # Fetch missing file
        try:
            content = fetch_fn()
        except Exception as exc:
            raise FileNotFoundError(
                f"Could not load {description} from file or API."
            ) from exc

        self._write_text(filename, content)
        return content.splitlines()

    # ----------------------------------------------------------------------
    # Specific loaders
    # ----------------------------------------------------------------------

    def _load_input_data(self):
        lines = self._load_or_fetch(
            "input_data",
            lambda: api.get_input(self.day),
            description="input data",
        )
        return self.process_data(lines)

    def _load_test_data(self, part: int):
        filename = self.test_data_paths[part - 1]
        lines = self._load_or_fetch(
            filename,
            lambda: api.get_test_data(self.day),
            description=f"test data for part {part}",
        )
        return self.process_data(lines)

    def _load_test_solution(self, part: int) -> int:
        filename = f"test_solution_{part}"

        # Try local file
        try:
            lines = self._read_lines(filename)
            if len(lines) != 1:
                raise ValueError(
                    f"{filename} must contain exactly one line, got {len(lines)}."
                )
            return int(lines[0].strip())
        except FileNotFoundError:
            pass

        # Fetch via API
        try:
            solution = api.get_test_solution(self.day, part)
        except Exception as exc:
            raise FileNotFoundError(
                f"Could not load test solution for part {part}."
            ) from exc

        self._write_text(filename, str(solution))
        return int(solution)

    # ----------------------------------------------------------------------
    # Running tests and solutions
    # ----------------------------------------------------------------------

    def _run_test(self, part: int) -> None:
        part_fn = getattr(self, f"part_{part}")
        expected = self._load_test_solution(part)
        data = self._load_test_data(part)

        try:
            result = part_fn(*data)
        except NotImplementedError:
            raise NotImplementedError(f"part_{part} is not implemented.")

        if result is None:
            raise AssertionError(f"part_{part} returned None.")
        if result != expected:
            raise AssertionError(
                f"Test for part {part} failed: expected {expected}, got {result}"
            )

    def _run_part(self, part: int):
        data = self._load_input_data()
        return getattr(self, f"part_{part}")(*data)

    def run(self):
        try:
            solved = api.number_of_parts_solved(self.day)
            can_submit = True
        except Exception:
            solved = 0
            can_submit = False

        for part in (1, 2):
            # Test
            try:
                self._run_test(part)
            except AssertionError as exc:
                print(exc)
                return
            except Exception as exc:
                raise RuntimeError(
                    f"Unexpected error during testing part {part}"
                ) from exc

            # Solve
            try:
                answer = self._run_part(part)
                print(f"Part {part}: {answer}")
            except Exception as exc:
                raise RuntimeError(f"Could not run part {part}") from exc

            # Submit
            if can_submit and solved < part:
                try:
                    api.submit_solution(self.day, part, answer)
                except Exception as exc:
                    raise RuntimeError(
                        f"Failed to submit solution for part {part}"
                    ) from exc
