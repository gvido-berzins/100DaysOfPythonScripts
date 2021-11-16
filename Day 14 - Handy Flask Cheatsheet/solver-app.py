import argparse
import os
import re

from flask import Flask, render_template, request
from unidecode import unidecode

app = Flask(__name__)

Q_REGEX = r"^([1-6][.]\d{1,3})[.]*\s(.*)$"
C_REGEX = r"^([A-D])[)].+$"
A_REGEX = r"^ANSWER: (\w{1})$"

SCRIPT_DIR = os.path.join(os.path.dirname(__file__))
DATA_DIR = os.path.join(SCRIPT_DIR, "data")
FILE = os.path.join(DATA_DIR, "aiken-import.txt")
CUSTOM = os.path.join(DATA_DIR, "aiken-custom.txt")


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("question")
    parser.add_argument("-t", "--tolerance", type=int, default=70)
    return parser.parse_args()


def load_cheats(file=FILE) -> list[str]:
    """Load the cheatsheets"""
    with open(file, "r") as f:
        CHEATS = [x.strip() for x in f.readlines()]
        return CHEATS


CHEATS = load_cheats()


def get_questions(cheats) -> dict:
    """Get the question number from the cheatsheet into a dictionary"""
    dict_ = {}
    for i, line in enumerate(cheats):
        match = re.search(Q_REGEX, line)
        if match:
            dict_[i] = match.group(0)
    return dict_


def get_question(question_index: int, CHEATS=CHEATS) -> str:
    """Get a question by its index"""
    return CHEATS[question_index]


def get_question_num_by_num(num, CHEATS=CHEATS) -> int:
    """Get a question number by line number from the cheatsheet"""
    for i, x in enumerate(CHEATS):
        match = re.search(Q_REGEX, x)
        if match:
            if match.group(1) == num:
                return i


def get_answer(question_index: int, CHEATS=CHEATS) -> str:
    """Get the answer by using the question number index"""
    return CHEATS[question_index + 5]


def get_choices(question_index: int, CHEATS=CHEATS) -> str:
    """Get the multiple choices by using the question index"""
    return "<br>".join(CHEATS[question_index + 1:question_index + 5])


def get_best_match(questions, question, tolerance=70) -> str:
    """Get the questions with the highest percentage"""
    best_score = 0
    question = unidecode(question)
    best_match = None
    possible_matches = []

    for i, question in questions.items():
        score = 0
        question = unidecode(question)
        words = question.lower().split(" ")
        word_count = len(words)

        target_words = question.lower().split(" ")

        for word in target_words:
            if word in words:
                score += 1

        percentage = round((score / word_count) * 100, 2)
        if percentage >= tolerance:
            possible_matches.append(i)

        if score > best_score:
            best_score = score
            best_match = i

    return best_match, possible_matches


def concat(previous_text, text) -> str:
    """Concatinate 2 strings together with an HTML linebreak"""
    return previous_text + str(text) + "<br>"


def give_answer(question, tolerance=70, CHEATS=CHEATS, custom=False):
    questions = get_questions(CHEATS)
    question_index, possible_matches = get_best_match(
        questions, question, tolerance
    )
    result = ""

    try:
        question = get_question(question_index, CHEATS=CHEATS)
        choices = get_choices(question_index, CHEATS=CHEATS)
        answer = get_answer(question_index, CHEATS=CHEATS)

        result = concat(
            result,
            '========------ <b style="color:#26DB79;">Best Batch</b> ------========',
        )
        result = concat(result, question)
        result = concat(result, choices)
        result = concat(result, f'<b style="color:green;">{answer}</b>')
        result = concat(result, "========================================")
        result = concat(result, "")

        result = concat(
            result,
            '======== <b style="color:#DD9F11">Other Possible Matches</b> ========',
        )
        if len(possible_matches) <= 1:
            result = concat(
                result,
                '<span style="color:red;"><b>[x] No other matches found</b></span>',
            )
        else:
            for match in possible_matches:
                if match == question_index:
                    continue
                question = get_question(match, CHEATS=CHEATS)
                choices = get_choices(match, CHEATS=CHEATS)
                answer = get_answer(match, CHEATS=CHEATS)

                result = concat(result, question)
                result = concat(result, choices)
                result = concat(
                    result, f'<b style="color:green;">{answer}</b>'
                )
                result = concat(result, "")
        result = concat(result, "========================================")

    except TypeError:
        result = concat(
            result, '<b style="color:crimson;">[!] Question not found</b>'
        )

    if custom:
        custom_list = load_cheats(file=CUSTOM)
        result = give_answer(
            question,
            tolerance=tolerance,
            CHEATS=custom_list,
            custom=False
        )

    return result


@app.route("/", methods=["GET", "POST"])
def main_page():
    result = ""
    if request.method == "POST":
        search = request.form["search"]
        tolerance = int(request.form["tolerance"]
                        ) if request.form["tolerance"] else 70
        checkbox = bool(request.form.getlist("custom"))

        result = give_answer(search, tolerance=tolerance, custom=checkbox)

        return render_template(
            "index.html", result=result, tolerance=tolerance
        )

    return render_template("index.html", result=result)
