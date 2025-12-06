import os
import re
from datetime import datetime
from typing import Optional

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()

YEAR = int(os.getenv("YEAR", datetime.now().year))
TOKEN = os.getenv("TOKEN")


# ----------------------------------------------------------------------
# Utility: HTTP Fetching
# ----------------------------------------------------------------------


class AOCRequestError(RuntimeError):
    """Raised when Advent of Code HTTP requests fail."""


def _session_cookie() -> dict[str, str]:
    if not TOKEN:
        raise ValueError("Missing TOKEN environment variable (session ID).")
    return {"Cookie": f"session={TOKEN}"}


def _aoc_url(day: int, *parts: str) -> str:
    path = "/".join(parts)
    if path:
        return f"https://adventofcode.com/{YEAR}/day/{day}/{path}"
    return f"https://adventofcode.com/{YEAR}/day/{day}"


def _fetch(
    day: int, *parts: str, method: str = "GET", data: Optional[dict] = None
) -> str:
    """
    Fetches a page from adventofcode.com and returns its text content.
    Raises AOCRequestError on failure.
    """
    url = _aoc_url(day, *parts)
    headers = _session_cookie()

    try:
        response = (
            requests.get(url, headers=headers)
            if method == "GET"
            else requests.post(url, headers=headers, data=data or {})
        )
    except requests.RequestException as exc:
        raise AOCRequestError(f"Network error fetching {url}") from exc

    if response.status_code != 200:
        raise AOCRequestError(f"HTTP {response.status_code} when fetching {url}")

    return response.text


def _get_day_html(day: int) -> BeautifulSoup:
    return BeautifulSoup(_fetch(day), "html.parser")


# ----------------------------------------------------------------------
# Input Fetching
# ----------------------------------------------------------------------


def get_input(day: int) -> str:
    """Returns the puzzle input for a given day."""
    try:
        text = _fetch(day, "input")
        return text.strip("\n")
    except AOCRequestError as exc:
        print(exc)
        return ""


def get_test_data(day: int) -> str:
    """Extracts the largest <code> block from the first article."""
    soup = _get_day_html(day)
    article = soup.find("article")
    if not article:
        return ""

    code_blocks = article.find_all("code")
    if not code_blocks:
        return ""

    largest = max(code_blocks, key=lambda c: len(c.get_text()))
    return largest.get_text().strip()


# ----------------------------------------------------------------------
# Test Solutions
# ----------------------------------------------------------------------


def _extract_test_solution(article: BeautifulSoup) -> Optional[str]:
    """
    Extract result in <em> or <code> blocks, checking common AOC patterns.
    """
    # Examples often highlight answers like: <code><em>42</em></code>
    for tag in reversed(article.find_all("code")):
        em = tag.find("em")
        if em and em.string:
            return em.string.strip()

    # Fallback patterns
    for em in reversed(article.find_all("em")):
        code = em.find("code")
        if code and code.string:
            return code.string.strip()

    return None


def get_test_solution(day: int, part: int) -> str:
    """Returns the example output for part 1 or 2 (if available)."""
    if part not in (1, 2):
        raise ValueError("Part must be 1 or 2")

    soup = _get_day_html(day)
    articles = soup.find_all("article")

    if part > len(articles):
        print(f"No article yet for part {part}")
        return ""

    solution = _extract_test_solution(articles[part - 1])
    if not solution:
        print(f"No test solution found for part {part}")
        return ""

    return solution


# ----------------------------------------------------------------------
# Submission Tracking
# ----------------------------------------------------------------------


def number_of_parts_solved(day: int) -> int:
    """
    Returns:
        0 → none solved
        1 → part 1 solved
        2 → both solved
    """
    soup = _get_day_html(day)

    form = soup.find("form", action=f"{day}/answer")
    if not form:
        return 2  # both solved

    level_input = form.find("input", {"name": "level"})
    if not level_input:
        raise ValueError("Could not find submission level in HTML.")

    # AOC uses level=1 for "about to submit part 1", so solved = level - 1
    return int(level_input.get("value")) - 1


# ----------------------------------------------------------------------
# Submission
# ----------------------------------------------------------------------


def _parse_submission_feedback(text: str) -> str:
    """
    Returns a human-readable message summarizing the submission result.
    """
    if "You gave an answer too recently" in text:
        time_left = re.search(r"You have (.+?) left", text)
        return f"Cooldown active. Wait {time_left.group(1) if time_left else 'a bit'}."

    if "That's not the right answer" in text:
        wait = re.search(r"lease wait (.+?) before trying again", text)
        return f"Incorrect answer. Wait {wait.group(1) if wait else 'a bit'}."

    if "That's the right answer" in text:
        return "Correct answer!"

    if "You don't seem to be solving the right level" in text:
        return "This part was already solved."

    return f"Unexpected submission response:\n{text}"


def submit_solution(day: int, level: int, answer: int | str) -> None:
    if level not in (1, 2):
        raise ValueError("Level must be 1 or 2")

    if number_of_parts_solved(day) >= level:
        print(f"Day {day} part {level} already solved.")
        return

    html = _fetch(day, "answer", method="POST", data={"level": level, "answer": answer})
    soup = BeautifulSoup(html, "html.parser")
    article = soup.find("article")

    if not article:
        print("Unexpected submission output.")
        print(html)
        return

    message = _parse_submission_feedback(article.get_text())
    print(message)
