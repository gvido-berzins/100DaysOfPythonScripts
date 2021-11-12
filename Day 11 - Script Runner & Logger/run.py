#!/usr/bin/env python3.9

import argparse
import logging
import os
import subprocess
from collections import namedtuple

PYTHON = "python3"
AUTO_MODE = "a"

SCRIPT_DIR = os.path.dirname(__file__)
LOG_DIR = os.path.join(SCRIPT_DIR, "logs")
LOG_FILE = os.path.join(LOG_DIR, "log.txt")
FAIL_LOG_FILE = os.path.join(LOG_DIR, "fail.txt")
PASS_LOG_FILE = os.path.join(LOG_DIR, "success.txt")
os.makedirs(LOG_DIR, exist_ok=True)

Logger = namedtuple("Logger", "root passer console")
CommandOutput = namedtuple("CommandOutput", "return_code stdout stderr")


def parse_args() -> argparse.Namespace:
    """Parse the command line arguments"""
    parser = argparse.ArgumentParser(
        description="Script for running and logging another Python script"
    )
    parser.add_argument("script", help="Target script filename")
    parser.add_argument(
        "paths",
        help="Script arguments, in my case FTP paths for processing"
    )
    return parser.parse_args()


def load_data(filename: str) -> str:
    """Load the contents of a file and return a string"""
    with open(filename, "r") as f:
        return f.read()


def format_file_contents_to_lines(data: str) -> list[str]:
    """Format file contents as a list of its lines"""
    return [_.strip() for _ in data.split("\n")]


def load_lines(filename: str) -> list[str]:
    """Return a list of lines from a file"""
    return format_file_contents_to_lines(load_data(filename))


def get_loggers() -> Logger:
    """Setup and return main logger and pass logger"""
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s %(name)-12s %(levelname)-8s %(message)s",
        datefmt="%d-%m %H:%M",
        filename=LOG_FILE,
        filemode="a",
    )
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        "%(name)-12s: %(levelname)-8s %(message)s"
    )
    console.setFormatter(formatter)

    formatter = logging.Formatter(
        fmt="%(asctime)s %(name)-12s %(levelname)-8s %(message)s",
        datefmt="%d-%m %H:%M"
    )

    fail_handler = logging.FileHandler(FAIL_LOG_FILE, mode="a")
    fail_handler.setLevel(logging.CRITICAL)
    fail_handler.setFormatter(formatter)
    pass_handler = logging.FileHandler(PASS_LOG_FILE, mode="a")
    pass_handler.setLevel(logging.INFO)
    pass_handler.setFormatter(formatter)

    pass_logger = logging.getLogger("pass")
    pass_logger.addHandler(pass_handler)
    logging.getLogger("").addHandler(fail_handler)
    logging.getLogger("").addHandler(console)
    logger = logging.getLogger("")
    return Logger(logger, pass_logger, console)


def log_execution_status(
    script, path, command_output: CommandOutput
) -> None:
    """Log execution status based on the return code"""
    if command_output.return_code:
        logger.root.critical(f"FAIL: {script} {path}")
    logger.passer.info(f"PASS: {script} {path}")
    logger.root.debug(
        f"STDOUT: {command_output.stdout};"
        f"STDERR: {command_output.stderr};"
        f"CODE: {command_output.return_code}"
    )


def run_script(filename: str, path: str) -> CommandOutput:
    """Run the script and perform logging"""
    args = [PYTHON, filename, AUTO_MODE, path]
    logger.root.debug(f"Running with args {args}")
    logger.root.debug("Process started")
    process = subprocess.Popen(
        args,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    logger.root.debug("Process ended")
    stdout, stderr = process.communicate()
    logger.root.debug("CommandOutput creation")
    return CommandOutput(process.returncode, stdout, stderr)


def run_script_for_all_paths(script, paths) -> None:
    """Run the script through a list of paths for its arguments"""
    for path in paths:
        logger.root.debug(f"Running '{script}' with '{path}'")
        command_output = run_script(script, path)
        log_execution_status(script, path, command_output)
        logger.root.debug("Finished.")


def main():
    script = args.script
    paths = load_lines(args.paths)
    run_script_for_all_paths(script, paths)


if __name__ == "__main__":
    logger = get_loggers()
    args = parse_args()
    main()
