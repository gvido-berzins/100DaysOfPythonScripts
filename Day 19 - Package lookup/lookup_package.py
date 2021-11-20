#!/usr/bin/env python3.9

import argparse
from dataclasses import dataclass, field
from pprint import pprint
from typing import Any, Protocol

import requests
from bs4 import BeautifulSoup

NOT_FOUND = "Not found"
PACKAGE_REPLACEMENT = "$PACKAGE"


@dataclass(order=True, frozen=True)
class Package:
    name: str
    repo: str = field(repr=False, compare=False)
    url: str = field(repr=False, compare=False)
    desc: str
    db: str


class PackageDatabase(Protocol):
    """Class representing the Package Database"""
    @classmethod
    def search(cls, package_name: str) -> list[Package]:
        ...

    @classmethod
    def extract_packages_from_search(cls,
                                     search_results: Any) -> list[Package]:
        ...


class ArchPackageDatabase:
    """Arch package repository database

    https://wiki.archlinux.org/title/Official_repositories_web_interface"""

    NAME = "Arch Repository"
    PACKAGE_INFO = "https://www.archlinux.org/packages/"
    SEARCH_ENDPOINT = "https://www.archlinux.org/packages/search/json/?q="

    @classmethod
    def search(cls, package_name: str) -> list[Package]:
        search_results = requests.get(cls.SEARCH_ENDPOINT +
                                      package_name).json()
        return cls.extract_packages_from_search(search_results)

    @classmethod
    def extract_packages_from_search(cls,
                                     search_results: Any) -> list[Package]:
        package_list = []
        for result in search_results.get("results", None):
            package_list.append(
                Package(
                    name=result["pkgname"],
                    repo=result["repo"],
                    url=result["url"],
                    desc=result["pkgdesc"],
                    db=cls.__name__,
                )
            )
        return list(set(package_list))


class AURPackageDatabase:
    """Arch User Repository database

    AUR uses their RPC to get the package info with JSON format
    https://aur.archlinux.org/rpc.php"""

    NAME = "Arch User Repository"
    BASE_URL = "https://aur.archlinux.org/"
    RPC = "rpc.php"
    SEARCH_ENDPOINT = "/rpc/?v=5&type=search&arg="

    @classmethod
    def search(cls, package_name: str) -> list[Package]:
        search_results = requests.get(
            cls.BASE_URL + cls.RPC + cls.SEARCH_ENDPOINT + package_name
        ).json()
        return cls.extract_packages_from_search(search_results)

    @classmethod
    def extract_packages_from_search(cls,
                                     search_results: Any) -> list[Package]:
        package_list = []
        for result in search_results.get("results", None):
            package_list.append(
                Package(
                    name=result["Name"],
                    repo=cls.BASE_URL[:-1] + result["URLPath"],
                    url=result["URL"],
                    desc=result["Description"],
                    db=cls.__name__,
                )
            )
        return list(set(package_list))


class ArtixPackageDatabase:
    """Class representing the Artix universe Package Database

    This package repository is found in an 'Index Of', BeautifulSoup needed
    https://universe.artixlinux.org/x86_64/"""

    NAME = "Artix Universe Repository"
    BASE_URL = "https://universe.artixlinux.org/"
    ARCH = "x86_64/"
    CSS_SELECTOR = f"pre>a[href$=zst][href*={PACKAGE_REPLACEMENT}]"

    @classmethod
    def search(cls, package_name: str) -> list[Package]:
        res = requests.get(cls.BASE_URL + cls.ARCH).text
        page = BeautifulSoup(res, "html.parser")
        search_results = page.select(
            cls.CSS_SELECTOR.replace(PACKAGE_REPLACEMENT, package_name)
        )
        return cls.extract_packages_from_search(search_results)

    @classmethod
    def extract_packages_from_search(cls,
                                     search_results: Any) -> list[Package]:
        package_list = []
        for result in search_results:
            package_filename = result.get("href")
            package_name = package_filename.replace(
                f"-{cls.ARCH[:-1]}.pkg.tar.zst", ""
            )
            package_list.append(
                Package(
                    name=package_name,
                    repo=NOT_FOUND,
                    url=cls.BASE_URL + cls.ARCH + package_filename,
                    desc=NOT_FOUND,
                    db=cls.__name__,
                )
            )
        return list(set(package_list))


class PyPiPackageDatabase:
    """Class representing the Python Package Index Database

    Simple 'BeautifulSoup' magic required, page consists of a tags
    https://pypi.org/simple/

    URL from the frontend
    https://pypi.org/project/<PACKAGE>/

    JSON API
    https://pypi.org/pypi/<PACKAGE>/json"""

    NAME = "Python Package Index Repository"
    BASE_URL = "https://pypi.org/"
    SIMPLE_ENDPOINT = "simple/"
    PROJECT_ENDPOINT = "project/"

    JSON_ENDPOINT = f"pypi/{PACKAGE_REPLACEMENT}/json"
    CSS_SELECTOR = f"a[href*={PACKAGE_REPLACEMENT}"

    @classmethod
    def search(cls, package_name: str) -> list[Package]:
        res = requests.get(cls.BASE_URL + cls.SIMPLE_ENDPOINT).text
        page = BeautifulSoup(res, "html.parser")
        result_set = page.find_all(
            lambda tag: tag.name == "a" and package_name in tag.text
        )
        search_results = cls.spider_result_set(result_set, package_name)
        return cls.extract_packages_from_search(search_results)

    @classmethod
    def extract_packages_from_search(cls,
                                     search_results: Any) -> list[Package]:
        """jq example of extracting from the JSON response:
        cat pypi-example.json |\
        jq '.info | [.name, .summary, .home_page, .package_url]'"""
        package_list = []
        for result in search_results:
            result = result["info"]
            package = Package(
                name=result["name"],
                repo=result["home_page"],
                url=result["package_url"],
                desc=result["summary"],
                db=cls.__name__,
            )
            if package not in package_list:
                package_list.append(package)

        return list(set(package_list))

    @classmethod
    def spider_result_set(cls, result_set, search_package) -> list[dict]:
        return [
            requests.get(
                cls.BASE_URL + cls.JSON_ENDPOINT.
                replace(PACKAGE_REPLACEMENT, search_package)
            ).json() for package_name in result_set
        ]


def filter_databases(databases: str) -> list[PackageDatabase]:
    return [
        database for database in ALL_DATABASES
        if database.__name__.lower() in parse_database_list(databases)
    ]


def parse_database_list(databases: str) -> list[str]:
    return databases.lower().replace(" ", "").split(",")


def search_databases(
    package_name: str, databases: list[PackageDatabase]
) -> None:
    """Search the all the enable databases in the ALL_DATABASES list or a
    filtered list"""
    for database in databases:
        print("\n# " + database.__name__)
        res = sorted(
            database.search(package_name),
            key=lambda x: x.name,
            reverse=True
        )
        pprint(res)


def parse_args():
    parser = argparse.ArgumentParser(
        description="Python package for querying packages from various"
        "repositories which include: Arch main, AUR, Artix universe, PyPi."
    )
    parser.add_argument("package_name", help="package name to search for")
    parser.add_argument(
        "-d",
        "--databases",
        help="List of comma separated database class names (any case)",
        default=None,
    )
    return parser.parse_args()


def main():
    package_name = args.package_name
    databases = (
        ALL_DATABASES
        if not args.databases else filter_databases(args.databases)
    )
    search_databases(package_name, databases)


if __name__ == "__main__":
    ALL_DATABASES = [
        PyPiPackageDatabase,
        ArchPackageDatabase,
        AURPackageDatabase,
        ArtixPackageDatabase,
    ]
    args = parse_args()
    main()
