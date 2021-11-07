from glob import glob
import subprocess
import shlex
import asyncio
import os
import json
import re


ENVIRONMENT_VARIABLES = ["SHELL", "PATH", "USER", "HOME"]
ENVIRONMENT_F = [
    "/etc/profile",
    "/etc/bashrc",
    "~/.profile",
    "~/.bash_profile",
    "~/.bashrc",
    "~/.bash_logout",
]

PERMISSION_MISCONFIGURATION_F = [
    "/etc/passwd",
    "/etc/shadow",
]

OTHER_FILES_F = [
    "/etc/hosts",
    "/etc/hostname",
    "/etc/groups"
]

ENUMERATION_F = [
    "/proc/version",
    "/etc/issue"
]

RELEASE_INFO_F = [
    "/etc/*-release",  # Operating System specific (arch-release)
    "/etc/lsb-release",
    "/etc/os-release"
]

KERNEL_VERSION_F = [
    "/proc/version"
]

SCHEDULES_TASKS_F = [
    "/etc/crontab",
    "/etc/cron*/*"
]

SSH_F = [
    "~/.ssh/authorized_keys",
    "~/.ssh/identity.pub",
    "~/.ssh/identity",
    "~/.ssh/id_rsa.pub",
    "~/.ssh/id_rsa",
    "~/.ssh/id_dsa.pub",
    "~/.ssh/id_dsa",
]

SUPPORTED_DEV_CMD = [
    "find / -name perl*",
    "find / -name python*",
    "find / -name gcc*",
    "find / -name cc",
]

SUDO_CMD = [
    "sudo -l",
]

SUDO_F = [
    "/etc/sudoers"
]


def jp(data):
    data = json.dumps(data, indent=2)
    print(data)
    return data


def load_data(filename):
    try:
        filename = os.path.expanduser(filename)
        with open(filename, 'r') as f:
            return f.read()
    except FileNotFoundError:
        # print(f"[X] File '{filename}' not found.")
        return ""


def parse_file_list(file_list):
    parsed_file_list = []

    for filename in file_list:
        if '*' in filename:
            parsed_file_list.extend(glob(filename))
            continue

        parsed_file_list.append(filename)
    return list(set(parsed_file_list))


def get_file_contents(file_list):
    file_list = parse_file_list(file_list)
    return [{path: load_data(path)} for path in file_list]


def get_file_statistics(path):
    try:
        full_path = os.path.expanduser(path)
        return os.stat(full_path)
    except FileNotFoundError:
        # print(f"[X] File '{filename}' not found.")
        return ""


def filter_empty(list_):
    return list(set(filter(None, list_)))


def get_permissions(file_list):
    file_list = filter_empty(file_list)
    return [{
            path: oct(
                get_file_statistics(path).st_mode & 0o777
            )} for path in file_list]


def get_writable_files(file_list):
    file_list = filter_empty(file_list)
    return [{
        path: "WRITEABLE"
    } for path in file_list if check_writable(path)]


def get_readable_files(file_list):
    file_list = filter_empty(file_list)
    return [{
        path: "READABLE"
    } for path in file_list if check_readable(path)]


def check_readable(path):
    return os.access(path, os.R_OK)


def check_writable(path):
    return os.access(path, os.W_OK)


async def run_command(command):
    process_output = subprocess.Popen(
        shlex.split(command),
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
    )
    output = process_output.stdout.read().decode("utf-8")
    return output


def create_command_tasks(command_list):
    return [asyncio.ensure_future(run_command(command))
            for command in command_list]


def get_environment_variables():
    return [{variable: os.environ.get(variable)}
            for variable in ENVIRONMENT_VARIABLES]


def get_environment_variables_from_file(filename):
    data = load_data(filename).split("\n")
    results = []
    for line in data:
        match = re.search(r'export (\w+)[=](\S*)', line.rstrip())
        if match:
            variable = match.group(1)
            value = trim_quotes(match.group(2))
            results.append({variable: value})
    return results


def get_environment_from_files(file_list):
    return [{filename: get_environment_variables_from_file(filename)}
            for filename in file_list]


def get_environment():
    results = []
    results.extend(get_environment_variables())
    results.extend(get_environment_from_files(ENVIRONMENT_F))
    return results


def trim_quotes(string):
    quotes = ['"', "'"]
    return string[1:-1] \
        if string[0] in quotes and string[1] in quotes \
        else string


def pt(action):
    print(f"==== {action.upper()} ====")


async def main():
    pt("Getting environment variables")
    environment_variables = get_environment()
    jp(environment_variables)

    pt("Getting system information")
    system_info = get_file_contents(
        ENUMERATION_F + RELEASE_INFO_F + KERNEL_VERSION_F + KERNEL_VERSION_F +
        SCHEDULES_TASKS_F
    )
    jp(system_info)

    pt("Checking for 'writable' files")
    permissions = get_writable_files(PERMISSION_MISCONFIGURATION_F)
    ssh_permissions = get_writable_files(SSH_F)
    jp(permissions + ssh_permissions)

    pt("Checking for 'readable' files")
    permissions = get_readable_files(PERMISSION_MISCONFIGURATION_F)
    ssh_permissions = get_readable_files(SSH_F)
    jp(permissions + ssh_permissions)

    pt("Checking for build tools and programming languages")
    command_tasks = create_command_tasks(SUPPORTED_DEV_CMD)
    command_output = await asyncio.gather(*command_tasks)
    jp(command_output)

    pt("Running super user commands")
    sudo_command_tasks = create_command_tasks(SUDO_CMD)
    sudo_command_output = await asyncio.gather(*sudo_command_tasks)
    jp(sudo_command_output)

    sudo_info = get_file_contents(SUDO_F)
    jp(sudo_info)

    pt("DONE")


if __name__ == "__main__":
    asyncio.run(main())

