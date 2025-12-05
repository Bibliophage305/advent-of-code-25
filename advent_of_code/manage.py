import argparse
import importlib
import os
from datetime import UTC, date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from dotenv import load_dotenv

load_dotenv()

YEAR = int(os.getenv("YEAR", datetime.now().year))
MAX_DAYS = int(os.getenv("MAX_DAYS", 25))

BASE_DIR = Path("advent_of_code")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def get_day_from_args() -> int | None:
    """
    Parse an optional day argument from CLI and validate it.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("day", nargs="?")
    args = parser.parse_args()

    day = int(args.day) if args.day is not None else None
    valid_days = {i for i in range(1, MAX_DAYS + 1)}

    if day is not None and day not in valid_days:
        raise ValueError(f"Day must be a number between 1 and {MAX_DAYS}.")
    return day


def human_readable_timedelta(delta) -> str:
    """
    Convert a timedelta into a compact "X hours and Y minutes" format.
    """
    days = delta.days
    hours, rem = divmod(delta.seconds, 3600)
    minutes, seconds = divmod(rem, 60)

    components = [
        (days, "day"),
        (hours, "hour"),
        (minutes, "minute"),
        (seconds, "second"),
    ]

    parts = [(v, name) for v, name in components if v > 0][:2]

    def fmt(v, u):
        return f"{v} {u}" + ("s" if v != 1 else "")

    match len(parts):
        case 2:
            return f"{fmt(*parts[0])} and {fmt(*parts[1])}"
        case 1:
            return fmt(*parts[0])
        case _:
            return "less than a second"


# ---------------------------------------------------------------------------
# Day creation
# ---------------------------------------------------------------------------

SOLVER_TEMPLATE = """import advent


class Solver(advent.Advent):
    def process_data(self, data):
        return [data]

    def part_1(self, data):
        pass

    def part_2(self, data):
        pass
"""


def _create_solver_file(day: int, skip_overwrite: bool = False) -> None:
    """
    Create the directory and solver.py file for a given day.
    Does *not* create input/test files — advent.py handles those dynamically.
    """
    day_dir = BASE_DIR / str(day)
    day_dir.mkdir(parents=True, exist_ok=True)

    solver_path = day_dir / "solver.py"

    if solver_path.exists() and not skip_overwrite:
        while True:
            resp = input(f"{solver_path} exists. Overwrite? (y/N): ").strip().lower()
            if resp in ("y", "n", ""):
                break
            print("Please enter y or n.")
        if resp not in ("y", "yes"):
            return
        solver_path.unlink()

    solver_path.write_text(SOLVER_TEMPLATE)


def _create_day(day: int, skip_overwrite: bool = False) -> None:
    """
    Create directory + solver template, but only if the puzzle has unlocked.
    """
    publish_dt = datetime.combine(
        date(int(YEAR), 12, int(day)),
        datetime.min.time(),
        tzinfo=ZoneInfo("America/New_York"),
    )

    now = datetime.now(UTC)

    if now < publish_dt:
        if not skip_overwrite:
            print(f"Day {day} is not released yet.")
            wait = human_readable_timedelta(publish_dt - now)
            print(f"Available in {wait}.")
        return

    _create_solver_file(day, skip_overwrite=skip_overwrite)


def create(day: int | None = None):
    """
    Main "create" function exposed to CLI.
    If no day is provided, initialize *all* days silently.
    """
    if day is None:
        for d in range(1, MAX_DAYS + 1):
            _create_day(d, skip_overwrite=True)
        return

    _create_day(day)


# ---------------------------------------------------------------------------
# Running solutions
# ---------------------------------------------------------------------------


def _run_day(day: str):
    """
    Imports and runs the solver module for a given day.
    """
    try:
        module = importlib.import_module(f"{day}.solver")
    except ModuleNotFoundError:
        print(f"Day {day} has not been created yet.")
        return

    solver = module.Solver(day)
    solver.run()


def run(day: str | None = None):
    """
    Run one day or all days.
    """
    if day is None:
        for d in range(1, MAX_DAYS + 1):
            print(f"Day {d}")
            _run_day(str(d))
            print()
        return

    _run_day(day)
