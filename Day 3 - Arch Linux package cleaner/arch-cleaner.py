from dataclasses import dataclass, field
from enum import Enum, auto
import argparse
import datetime
import json
import os


BINARY_DIRS = [
    "/usr/bin",
    "/usr/local/bin",
    "/home/gny/.local/bin/"
]

DESKTOP_APP_DIRS = [
    "/usr/share/applications/",
    "/home/gny/.local/share/applications/",
    "/home/gny/.gnome/apps/",
    "/home/gny/.jdks/"
]


def jp(data, indent=2) -> str:
    """List data using json.dumps"""
    json_dump = json.dumps(data, indent=indent)
    print(json_dump)
    return json_dump


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Simple system cleaner for Linux")
    parser.add_argument('action', choices=["list", "clean"])
    parser.add_argument(
        'scope',
        choices=["all", "applications", "binaries"],
        default="all"
    )
    return parser.parse_args()


def perform_action(action: str, scope: str) -> None:
    """Action parser"""
    directories = create_scope(scope)

    if action == 'list':
        start_list(directories)

    if action == 'clean':
        start_clean(directories)


def create_scope(scope: str) -> list[str]:
    """Return the directories based on the given scope"""
    if scope == 'applications':
        return DESKTOP_APP_DIRS

    if scope == 'binaries':
        return BINARY_DIRS

    return BINARY_DIRS + DESKTOP_APP_DIRS


def start_list(scope):
    manager = SoftwareManager(
        action="list",
        scope=scope,
    )
    manager.gather_packages()
    manager.list_packages()


def start_clean(scope):
    pass


class PackageType(Enum):
    """Enum representing a package type"""
    BINARY = "Binary"
    APPLICATION = "Application"


@dataclass
class Package:
    """Dataclass representing a package"""
    type_: str
    name: str
    location: str
    date_last_modified: str
    date_created: str

    def __str__(self):
        return f"""---
Type:\t\t{self.type_.value}
Name:\t\t{self.name}
Location:\t{self.location}
Created:\t{parse_timestamp(self.date_created)}
Last Modified:\t{parse_timestamp(self.date_last_modified)}
---"""


def parse_timestamp(timestamp):
    timestamp = datetime.datetime.fromtimestamp(timestamp)
    return timestamp.strftime('%Y-%m-%d %H:%M:%S')


@dataclass
class SoftwareManager:
    """Dataclass acting as the software manager"""
    action: str
    scope: list[str]
    packages: list[Package] = field(default_factory=list)

    def gather_packages(self) -> None:
        """Gather all packages from the defined scope"""
        for directory in self.scope:
            if directory in DESKTOP_APP_DIRS:
                package_type = PackageType.APPLICATION
            else:
                package_type = PackageType.BINARY

            for package in os.listdir(directory):
                full_path = os.path.join(directory, package)
                try:
                    stat_obj = os.stat(path=full_path)
                except:
                    continue

                self.packages.append(
                    Package(
                        type_=package_type,
                        name=package,
                        location=directory,
                        date_created=stat_obj.st_ctime,
                        date_last_modified=stat_obj.st_mtime,
                    )
                )

    def list_packages(self) -> None:
        if bool(self.packages):
            for package in self.packages:
                print(package)
        else:
            print("No packages gathered.")


def main():
    print("=== LINUX CLEANER ===")
    print(f"Performing action '{args.action}'\nwith scope '{args.scope}'\n")
    perform_action(args.action, args.scope)
    print("===     DONE      ===")


if __name__ == "__main__":
    args = parse_args()
    main()
