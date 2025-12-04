import os
import requests
from datetime import datetime
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import re

load_dotenv()

YEAR = os.getenv("YEAR", datetime.now().year)

def _fetch_url(day, parts, method="GET", data=None):
    if not os.getenv("TOKEN"):
        raise ValueError("No token found. Please set the TOKEN environment variable")
    url = f"https://adventofcode.com/{int(YEAR)}/day/{day}"
    for part in parts:
        url += f"/{part}"
    headers = {"Cookie": f"session={os.getenv('TOKEN')}"}
    if method == "GET":
        return requests.get(url, headers=headers)
    elif method == "POST":
        if data is None:
            data = {}
        return requests.post(url, headers=headers, data=data)
    else:
        raise ValueError("Unsupported HTTP method")

def _get_html_content(day):
    return _fetch_url(day, []).text

def get_input(day):
    response = _fetch_url(day, ["input"])

    if response.status_code == 200:
        return response.text.strip()
    else:
        print(
            f"Failed to retrieve input for day {day}. Status code: {response.status_code}"
        )
        return ""

def get_test_data(day):
    soup = BeautifulSoup(_get_html_content(day), "html.parser")
    largest_code_tag = max(soup.find_all("code"), key=lambda tag: len(tag.get_text()))
    return largest_code_tag.get_text().strip() if largest_code_tag else ""

def get_test_solution(day, part):
    if part not in [1, 2]:
        raise ValueError("Part must be 1 or 2")
    soup = BeautifulSoup(_get_html_content(day), "html.parser")
    articles = soup.find_all("article")
    if part > len(articles):
        print(f"No test solution found for part {part} yet, have you completed the previous part?")
        return ""
    code_tags = articles[part - 1].find_all("code")
    for code_tag in reversed(code_tags):
        if code_tag.em and code_tag.em.string:
            return code_tag.em.string.strip()
    return ""

def number_of_parts_solved(day):
    soup = BeautifulSoup(_get_html_content(day), "html.parser")
    submission_form = soup.find("form", {"action": f"{day}/answer"})
    if submission_form is None:
        return 2
    input_level_element = submission_form.find("input", {"name": "level"})
    if input_level_element is None:
        raise ValueError("Could not find level input in submission form")
    level = input_level_element.get("value")
    return int(level) - 1

def submit_solution(day, level, solution):
    if level not in [1, 2]:
        raise ValueError("Level must be 1 or 2")
    if number_of_parts_solved(day) >= level:
        print(f"Part {level} for day {day} has already been solved.")
        return
    payload = {"level": level, "answer": solution}
    response = _fetch_url(day, ["answer"], method="POST", data=payload)
    if response.status_code != 200:
        print(
            f"Failed to submit solution for day {day}. Status code: {response.status_code}"
        )
        return
    soup = BeautifulSoup(response.text, "html.parser")
    message_text = soup.find("article").find("p").get_text()
    if message_text.startswith("You gave an answer too recently"):
        timeout_remaining = re.search(r"(?<=You have ).+(?= left)", message_text)
        timeout_message = timeout_remaining.group(0) if timeout_remaining else "a while"
        print(f"Currently in a cooldown period. Please wait {timeout_message} before trying again.")
        return
    elif message_text.startswith("That's not the right answer"):
        timeout_remaining = re.search(r"(?<=lease wait ).+(?= before trying again)", message_text)
        timeout_message = timeout_remaining.group(0) if timeout_remaining else "a while"
        print(f"Incorrect solution. Please wait {timeout_message} before trying again.")
        return
    elif message_text.startswith("That's the right answer!"):
        print(f"Correct! Solution for day {day}, part {level} successfully submitted.")
        return
    elif message_text.startswith("You don't seem to be solving the right level"):
        print(f"Part {level} for day {day} has already been solved.")
        return
    print("Unexpected response when submitting solution:")
    print(response.text)

if __name__ == "__main__":
    day = 4
    part = 2
    print(get_test_solution(day, part))
