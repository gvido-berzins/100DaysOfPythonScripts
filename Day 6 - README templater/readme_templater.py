#!/usr/bin/env python3.9

import argparse
import cmd
import os
import tempfile
import traceback
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from subprocess import call

SCRIPT_NAME = os.path.basename(__file__)
SCRIPT_DIR = os.path.dirname(SCRIPT_NAME)
EDITOR = os.environ.get("EDITOR", "vim")

BASE_TEMPLATE = """---
Author: %AUTHOR%
Date: %DATE%
---

%DESCRIPTION%

## Prerequisites

%PREREQUISITES%

## Usage

%USAGE%
"""

DEFAULT_USAGE = f"Run the script with Python\n\n```\npython {SCRIPT_NAME}\n```"
DEFAULT_STDLIB = (
    "No need to install additional libraries, only standard library was used."
)


class Shell(cmd.Cmd):
    """Class representing the command-line for adding additional headers"""

    intro = "Additional field shell."
    prompt = "\\ >_< / .: "
    sections = ""

    # ----- basic turtle commands -----
    def do_sect(self, arg):
        """Create a new section for the README.md"""
        self.sections += craft_additional_sections(
            section=arg, content=get_value_from_editor()
        )
        self.sections += "\n\n"

    def do_exit(self, arg):
        """Exit the shell"""
        return True


def craft_additional_sections(section: str, content: str, level=2) -> str:
    """Craft additional sections and return the results"""
    section_level = "#" * level
    section_title = f"{section_level} {section}"
    return f"{section_title}\n\n{content}"


def get_value_from_editor(initial_message=b"") -> str:
    """Open the editor and get the written contents"""
    with tempfile.NamedTemporaryFile(suffix=".tmp") as tf:
        tf.write(initial_message)
        open_editor(tf.name)
        return tf.read().decode("utf-8").rstrip()


def open_editor(filename) -> None:
    """Opens the EDITOR"""
    call([EDITOR, filename])


class Placeholder(Enum):
    AUTHOR = "AUTHOR"
    DATE = "DATE"
    DESCRIPTION = "DESCRIPTION"
    PREREQUISITES = "PREREQUISITES"
    USAGE = "USAGE"


@dataclass
class Template:
    """Dataclass representing a template"""

    destination: str
    author: str
    date: str
    description: str = field(default="")
    prerequisites: str = field(default="")
    usage: str = field(default="")

    filename: str = field(default="README.md")
    base: str = field(default=BASE_TEMPLATE)
    contents: str = field(default=BASE_TEMPLATE)
    path: str = field(default="")
    additional_sections: str = field(default="")

    def __post_init__(self):
        if not self.path:
            self.path = os.path.join(self.destination, self.filename)

    def __str__(self):
        return f"{self.contents}"


class TemplateEngine:
    """Class representing the engine that creates the template"""
    def create_template(self, template: Template):
        """Create a new template"""
        self.generate_template_contents(template)
        write_file(template.path, template.contents)

    def generate_template_contents(self, template: Template) -> None:
        """Replace the placeholder contents with the template attribute
        values and return the new contents"""
        text = template.base
        replace = self.replace
        ph = Placeholder

        text = replace(text, ph.AUTHOR, template.author)
        text = replace(text, ph.DATE, template.date)
        text = replace(text, ph.DESCRIPTION, template.description)
        text = replace(text, ph.PREREQUISITES, template.prerequisites)
        text = replace(text, ph.USAGE, template.usage)
        text += template.additional_sections
        template.contents = text

    def replace(
        self, text: str, placeholder: Placeholder, value: str
    ) -> str:
        """Replace a placeholder with a value"""
        return text.replace(f"%{placeholder.value}%", value)


def get_current_date(date_format="%d.%m.%Y"):
    return datetime.now().strftime(date_format)


def write_file(path, data):
    with open(path, "w") as f:
        f.write(data)


def prompt_for(item) -> str:
    """Prompt for something specific"""
    answer = input(f"{item}: ")
    return "" if not answer else answer


def prompt_yn(message, answer=False) -> bool:
    """Prompt for an 'y/n' answer"""
    if answer:
        return True

    while answer not in [_ for _ in "yYnN"]:
        answer = input(f"{message} (y/n) ")

    if answer.lower() == "y":
        return True

    return False


def do_prefills(template):
    ph = Placeholder
    template.description = prompt_for(ph.DESCRIPTION)

    prerequisites = prompt_for(ph.PREREQUISITES)
    if prerequisites == "std":
        template.prerequisites = DEFAULT_STDLIB
    else:
        template.prerequisites = (
            prerequisites + "\n\n```\npip install -r requirements\n```"
        )

    usage = prompt_for(ph.USAGE)
    if not usage:
        template.usage = DEFAULT_USAGE
    else:
        template.usage = usage


def do_additional_fields(template):
    shell = Shell()
    shell.cmdloop()
    template.additional_sections = f"\n{shell.sections}"


def start_template_prompt() -> Template:
    """Start an interactive template prompt"""
    template = Template(
        author=args.author,
        date=args.date,
        destination=args.destination,
    )

    if args.noprompt:
        return template

    if not args.nopre and prompt_yn(
        "Do you want prefills?", answer=args.prefills
    ):
        do_prefills(template)

    if not args.noadd and prompt_yn(
        "Do you want additional fields?", answer=args.additional
    ):
        do_additional_fields(template)

    return template


def parse_args():
    parser = argparse.ArgumentParser(
        description=""
        "Python script that creates a README.md from a base template"
        "so that it's easier to repeat the process."
    )
    parser.add_argument(
        "-d",
        "--destination",
        help="README destination",
        default=os.getcwd()
    )
    parser.add_argument(
        "-a", "--author", help="README author", default="Gvido Bērziņš"
    )
    parser.add_argument(
        "--date", help="Creation date", default=get_current_date()
    )
    parser.add_argument(
        "-p",
        "--prefills",
        help="Prefill base sections",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "--nopre",
        help="Don't prefill base sections",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "--noadd",
        help="Don't create additional sections",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "--additional",
        help="Create additional sections",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "-n",
        "--noprompt",
        help="Create a bare template",
        action="store_true",
        default=False,
    )
    return parser.parse_args()


def main():
    try:
        template = start_template_prompt()
        engine = TemplateEngine()

        print("> Creating template")
        engine.create_template(template)
        print(template)

    except KeyboardInterrupt:
        print("\n\n> KeyboardInterrupt, exiting.")
        exit()

    except Exception:
        print("Something went wrong.")
        traceback.print_exc()

    finally:
        print("Done.")


if __name__ == "__main__":
    args = parse_args()
    main()
