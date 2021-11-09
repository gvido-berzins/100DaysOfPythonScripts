import argparse
import os
from enum import Enum, auto

import git

DEFAULT_KEYWORDS = ["secret", "key", "api", "token"]


class Case(Enum):
    LOWER = auto()
    UPPER = auto()
    NONE = auto()


class Sensitivity(Enum):
    SENSITIVE = auto()
    INSENSITIVE = auto()


def clone_a_repository(url, dest) -> None:
    """Clone a git repository"""
    return git.Repo.clone_from(url, dest)


def get_the_repository(url):
    """Get the repository locally"""
    try:
        return git.Repo(url)
    except git.exc.NoSuchPathError:
        print(
            "No such repository locally, did you mean to clone?\n"
            "Use -c, --clone flag instead if so"
        )
        exit()


def git_show(repo, sha):
    """Run git show with the given sha"""
    return repo.git.show(sha)


def parse_show(show, sensitivity: Sensitivity):
    """Parse git show based on the case sensitivity"""
    if sensitivity == Sensitivity.INSENSITIVE:
        return show.lower()
    return show


def parse_keyword(keyword: str, case: Case) -> str:
    """Parse keyword based on the case"""
    if case.LOWER:
        return keyword.lower()
    if case.UPPER:
        return keyword.upper()
    return keyword


def find_secrets_in_commits(
    repo: git.Repo,
    commits: git.Repo.commit,
    case: Case,
    sensitivity: Sensitivity,
    keywords: list[str] = DEFAULT_KEYWORDS,
) -> list[git.Repo.commit]:
    secrets = []
    shows = [git_show(repo, commit.hexsha) for commit in commits]

    for show in shows:
        for keyword in keywords:
            keyword = parse_keyword(keyword, case)
            show = parse_show(show, sensitivity)
            found = show.find(keyword)

            if found > 0 and show not in secrets:
                secrets.append(show)

    return secrets


def parse_args():
    parser = argparse.ArgumentParser(
        description="Git commit secret finder"
    )
    parser.add_argument(
        "repository", help="URL or the path to the git repository"
    )
    parser.add_argument(
        "-c", "--clone", help="Clone a repository", action="store_true"
    )
    parser.add_argument(
        "-s",
        "--sensitive",
        help="Case sensitive search",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "-u",
        "--upper",
        help="Search for the keywords in uppercase",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "-l",
        "--lower",
        help="Search for the keywords in lowercase",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "-k",
        "--keywords",
        help="Comma separated list of keywords to search for",
        default=DEFAULT_KEYWORDS,
    )
    return parser.parse_args()


def parse_keywords(keywords) -> list[str]:
    """Parse comma separated keywords"""
    if DEFAULT_KEYWORDS == args.keywords:
        return DEFAULT_KEYWORDS

    parsed_keywords = [_.rstrip().lstrip() for _ in keywords.split(",")]
    print(f"Parsed keywords: {parsed_keywords}")
    return parsed_keywords


def dump_secrets(secrets):
    if not bool(secrets):
        print("\n\nNo secrets found.")
        return

    print("\n\n=== SECRETS FOUND ===")
    print(f"Count of commits with secrets: {len(secrets)}")

    for secret in secrets:
        print("_______________________________")
        print(secret)
        print("_______________________________")


def parse_case() -> Case:
    if args.upper:
        return Case.UPPER
    if args.lower:
        return Case.LOWER
    return Case.NONE


def parse_sensitivity() -> Sensitivity:
    if args.sensitive:
        print("+ Case sensitive")
        return Sensitivity.SENSITIVE
    print("- Case insensitive")
    return Sensitivity.INSENSITIVE


def action_print(action):
    print("\n======================================")
    print(str(action).upper())
    print("======================================")


def main():
    repository = args.repository.rstrip("/")
    directory = os.path.basename(repository).replace(".git", "")
    keywords = parse_keywords(args.keywords)
    case = parse_case()
    sensitivity = parse_sensitivity()

    if args.clone:
        action_print("> Cloning the repository <")
        repo = clone_a_repository(repository, directory)
    else:
        action_print("> Getting the repository locally <")
        repo = get_the_repository(directory)

    commits = list(repo.iter_commits("--all"))

    secrets = find_secrets_in_commits(
        repo, commits, case, sensitivity, keywords=keywords
    )
    dump_secrets(secrets)


if __name__ == "__main__":
    args = parse_args()
    action_print(args)
    main()
