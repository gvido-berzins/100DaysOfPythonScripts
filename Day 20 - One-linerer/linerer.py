#!/usr/bin/env python3

import argparse
import base64

import pyperclip

FILENAME = "script.ps1"
# PREFIX = "powershell.exe -NoProfile -EncodedCommand"
# PREFIX = "powershell -nop -enc"
PREFIX = ""
END_SEPARATOR = ";"
COMMENT_SYMBOL = "#"


def load(filename: str = FILENAME) -> list[str]:
    """Load the script file"""
    with open(filename, "r") as f:
        return list(filter(None, f.read().split("\n")))


def make_oneliner(script: list[str]) -> str:
    """Create a simple one-liner from a list of the script lines"""

    parsed_script = ""

    for i, line in enumerate(script):
        text = line.strip()
        if text.startswith(COMMENT_SYMBOL):
            continue
        try:
            next_text = script[i + 1].strip()
        except IndexError:
            next_text = script[i].strip()

        symbols = "{}"
        if text not in symbols and next_text not in symbols:
            text = line + END_SEPARATOR
        parsed_script += text

    return parsed_script


def make_multiline(script: list[str]) -> str:
    """Create a simple one-liner from a list of the script lines"""
    return "\n".join(script)


def encode(data: str) -> str:
    """Encode the script one-liner using base64 encoding"""
    base64_string = base64.b64encode(data.encode("utf-8"))
    return base64_string.decode()


def copy_payload(
    payload: str, custom_prefix: str = "", noprefix: bool = False
) -> str:
    """Copy the script to the clipboad and return it"""
    if not noprefix:
        payload = f"{PREFIX} {payload}"

    if custom_prefix and not noprefix and PREFIX not in payload:
        payload = f"{args.prefix} {payload}"

    pyperclip.copy(payload)
    print(f"COPIED: | {payload} |")
    return payload


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-f",
        "--file",
        help=f"Filename for the powershell script, defaults to {FILENAME}",
        default=FILENAME,
    )
    parser.add_argument(
        "-p",
        "--prefix",
        help=f"Prefix for the script, defaults to {PREFIX}",
        default=PREFIX,
    )
    parser.add_argument(
        "-n",
        "--noprefix",
        action="store_true",
        help="Don't use prefix",
        default=False
    )
    parser.add_argument(
        "-d",
        "--noencode",
        action="store_true",
        help="Don't encode in base64",
        default=False,
    )
    parser.add_argument(
        "-m",
        "--noline",
        action="store_true",
        help="Prevent one-liner",
        default=False
    )
    parser.add_argument(
        "-c",
        "--nocopy",
        action="store_true",
        help="Don't copy to clipboard",
        default=False,
    )
    return parser.parse_args()


def main():
    script = load(filename=args.file)

    if not args.noline:
        script = make_oneliner(script)

    if isinstance(script, list):
        script = make_multiline(script)

    if not args.noencode and not args.noline:
        script = encode(script)

    copy_payload(script, custom_prefix=args.prefix, noprefix=args.noprefix)


if __name__ == "__main__":
    args = parse_args()
    print(args)
    main()
