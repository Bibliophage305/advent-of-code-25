import argparse
import importlib
import pathlib
import requests
from functools import cache
from bs4 import BeautifulSoup
import os
from datetime import datetime, date, UTC
from pytz import timezone
from dotenv import load_dotenv

load_dotenv()

YEAR = os.getenv("YEAR", datetime.now().year)

def _fetch_url(day, parts):
    if not os.getenv("TOKEN"):
        raise ValueError("No token found. Please set the TOKEN environment variable")
    url = f"https://adventofcode.com/{int(YEAR)}/day/{day}"
    for part in parts:
        url += f"/{part}"
    return requests.get(url, headers={"Cookie": f"session={os.getenv('TOKEN')}"})


def _get_input(day):
    response = _fetch_url(day, ["input"])

    if response.status_code == 200:
        return response.text.strip()
    else:
        print(
            f"Failed to retrieve input for day {day}. Status code: {response.status_code}"
        )
        return ""


@cache
def _get_html_content(day):
    return _fetch_url(day, []).text


def _get_test_data(day):
    soup = BeautifulSoup(_get_html_content(day), "html.parser")
    largest_code_tag = max(soup.find_all("code"), key=lambda tag: len(tag.get_text()))
    return largest_code_tag.get_text().strip() if largest_code_tag else ""


def _get_test_solution(day):
    soup = BeautifulSoup(_get_html_content(day), "html.parser")
    code_tags = soup.find_all("code")
    for code_tag in reversed(code_tags):
        if code_tag.em and code_tag.em.string:
            return code_tag.em.string.strip()
    return None


def _get_day_from_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("day", nargs="?")
    args = parser.parse_args()
    day = args.day
    if day is not None and day not in map(str, range(1, 26)):
        raise ValueError("Day must be a number between 1 and 25")
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
    part_1_test_solution = {_get_test_solution(day)}
    part_2_test_solution = None

    def process_data(self, data):
        return [data]

    def part_1(self, data):
        pass

    def part_2(self, data):
        pass
""",
        filename_prefix + "test": _get_test_data(day),
        filename_prefix + "input": _get_input(day),
    }
    _get_test_data(day)
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


def create():
    day = _get_day_from_args()
    if day is None:
        for day in range(1, 26):
            _create_day(str(day), skip_overwrite=True)
        return
    try:
        day = _get_day_from_args()
    except ValueError as e:
        print(e)
        return
    _create_day(day)


def _run_day(day):
    try:
        module = importlib.import_module(f"advent_of_code.{day}.solver")
    except ModuleNotFoundError as e:
        print(f"Day {day} hasn't been created yet")
        return
    s = module.Solver(day)
    s.run()


def run():
    day = _get_day_from_args()
    if day is None:
        for day in range(1, 26):
            print(f"Day {day}")
            _run_day(str(day))
            print()
        return
    try:
        day = _get_day_from_args()
    except ValueError as e:
        print(e)
        return
    _run_day(day)
