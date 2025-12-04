import argparse
import importlib
import pathlib
import os
from datetime import datetime, date, UTC
from pytz import timezone
from dotenv import load_dotenv

import api

load_dotenv()

YEAR = os.getenv("YEAR", datetime.now().year)
MAX_DAYS = int(os.getenv("MAX_DAYS", 25))


def get_day_from_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("day", nargs="?")
    args = parser.parse_args()
    day = args.day
    if day is not None and day not in map(str, range(1, MAX_DAYS + 1)):
        raise ValueError(f"Day must be a number between 1 and {MAX_DAYS}")
    return day


def _human_readable_timedelta(delta):
    days = delta.days
    hours, remainder = divmod(delta.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    def format_unit(value, unit):
        if value == 1:
            return f"{value} {unit}"
        else:
            return f"{value} {unit}s"

    components = []
    if days > 0:
        components.append((days, "day"))
    if hours > 0:
        components.append((hours, "hour"))
    if minutes > 0:
        components.append((minutes, "minute"))
    if seconds > 0:
        components.append((seconds, "second"))

    components = components[:2]

    if len(components) == 2:
        return f"{format_unit(*components[0])} and {format_unit(*components[1])}"
    elif len(components) == 1:
        return format_unit(*components[0])
    else:
        return "less than a second"


def _create_day(day, skip_overwrite=False):
    publish_date = datetime.combine(
        date(int(YEAR), 12, int(day)),
        datetime.min.time(),
        tzinfo=timezone("US/Eastern"),
    )
    now = datetime.now(UTC)
    if now < publish_date:
        if not skip_overwrite:
            print(f"Day {day} hasn't been published yet!")
            print(
                f"You have to wait for {_human_readable_timedelta(publish_date - now)}"
            )
        return
    filename_prefix = f"advent_of_code/{day}/"
    pathlib.Path(filename_prefix).mkdir(parents=True, exist_ok=True)
    filenames = {
        filename_prefix
        + "solver.py": f"""from advent_of_code import advent


class Solver(advent.Advent):
    def process_data(self, data):
        return [data]

    def part_1(self, data):
        pass

    def part_2(self, data):
        pass
""",
        filename_prefix + "test_data": api.get_test_data(day),
        filename_prefix + "input_data": api.get_input(day),
        filename_prefix + "test_solution_1": api.get_test_solution(day, 1),
    }
    for filename, default_content in filenames.items():
        if pathlib.Path(filename).is_file():
            if skip_overwrite:
                continue
            while True:
                token = input(f"{filename} already exists, overwrite? (y/N): ")
                match token.strip():
                    case "y" | "Y":
                        overwrite = True
                        break
                    case "" | "n" | "N":
                        overwrite = False
                        break
                    case _:
                        print("Options are (y/n)")
            if not overwrite:
                continue
            pathlib.Path(filename).unlink()
        with open(filename, "w") as f:
            f.write(default_content)


def create(day=None):
    if day is None:
        for day in range(1, MAX_DAYS + 1):
            _create_day(str(day), skip_overwrite=True)
        return
    _create_day(day)


def _run_day(day):
    try:
        module = importlib.import_module(f"{day}.solver")
    except ModuleNotFoundError as e:
        print(f"Day {day} hasn't been created yet")
        return
    parts_solved = api.number_of_parts_solved(int(day))
    for part in (1, 2):
        if part == 2 and parts_solved == 0:
            continue
        filename = f"advent_of_code/{day}/test_solution_{part}"
        if os.path.isfile(filename):
            with open(filename, "r") as f:
                content = f.read().strip()
                if content:
                    continue
        with open(filename, "w") as f:
            test_solution = api.get_test_solution(int(day), part)
            f.write(str(test_solution))
    s = module.Solver(day)
    s.run()


def run(day=None):
    if day is None:
        for day in range(1, MAX_DAYS + 1):
            print(f"Day {day}")
            _run_day(str(day))
            print()
        return
    _run_day(day)
