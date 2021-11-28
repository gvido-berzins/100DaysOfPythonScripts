#!/usr/bin/python3.9

import asyncio
import re
import sys
import traceback
from urllib import parse

import httpx

PLACEHOLDER = "SPLURT"
TARGETS = ["evn", "tag"]
USAGE = f"usage: python splurt.py <vuln-url={PLACEHOLDER}> <{TARGETS}>"


class RequestHandler:
    def __init__(self, url):
        self.url = url

    def __repr__(self):
        return f"{self.__class__.__name__}({self.url})"

    def start_fuzz(self, targets: list[str]) -> list[httpx.Response]:
        """Start the fuzzer asynchronously"""
        return asyncio.run(self.mas_request(targets))

    async def mas_request(self,
                          targets: list[str]) -> list[httpx.Response]:
        """Perform fuzzing on a list of targets"""
        try:
            async with httpx.AsyncClient() as client:
                tasks = (client.get(url) for url in targets)
                resps = await asyncio.gather(*tasks)

        except (httpx.ConnectTimeout, AttributeError) as e:
            try:
                traceback.print_tb(e)
            except AttributeError:
                print("Something went wrong.")
        return self.format_responses(resps)

    def build_targets(self, wordlist: list[str]):
        """Replace the placholder with the worlist items"""
        return [self.url.replace(PLACEHOLDER, param) for param in wordlist]

    def format_responses(self, resps: list[httpx.Response]):
        """Filter out None from the responses"""
        return list(
            filter(None, [self.format_response(res) for res in resps])
        )

    def format_response(self, res: httpx.Response):
        if res.status_code == 200:
            return {
                "res_text": res.text,
                "res_url": res.url,
                "res_code": res.status_code,
            }
        return None


class Formatter:
    """
    Format the responses for a friendly output
    """
    def __init__(self, res):
        self.res = res

    def __repr__(self):
        return f"{self.__class__.__name__}({self.res})"

    def format_response(self, res: dict, param: str = "tag"):
        """Format the return HTTP response"""
        res_text = res["res_text"]
        res_url = parse.unquote(str(res["res_url"]))
        res_code = res["res_code"]
        res_word_len = self.count_words(res_text)
        res_char_len = len(res["res_text"])

        if param == "attr":
            regex = r".*body (\w+)=alert.*"
        else:
            regex = r".*<(\w+)>.*$"

        try:
            value = re.search(regex, res_url).group(1)
        except AttributeError:
            value = "Not found"

        return "\n".join(
            [
                f"URL: {res_url}",
                f"{param}: {value}",
                f"Response: {res_code}",
                f"char len: {res_char_len}",
                f"word len: {res_word_len}",
                "+++++++++++++++++++++++++++++++",
            ]
        )

    def print_results(
        self,
        responses: dict,
        what_exclude: str = "char",
        exclude_count: str = "20",
    ) -> None:
        """Print the response, excluding the amount of characters or
        words"""
        for res in responses:
            results = self.format_response(res)
            if "{what_exclude} len: " + str(exclude_count) not in results:
                print(results)

    @staticmethod
    def count_words(words: list[str]) -> int:
        """Return the count of words from the response"""
        wordlist = []
        for word in words:
            if not str.isalnum(word):
                for character in word:
                    if not str.isalnum(character):
                        word = word.replace(character, "")
            wordlist.append(word)
        return len(list(filter(None, wordlist)))


class FileHandler:
    def __init__(self, type_):
        self.type_ = type_

    def __repr__(self):
        return f"{self.__class__.__name__}({self.type_})"

    def get_wordlist(self):
        """Get the wordlist filename based on the given target"""
        if self.type_ == "evn":
            return "events"
        elif self.type_ == "tag":
            return "tags"

    def load_wordlist(self) -> list[str]:
        """Return the wordlist based on the type of fuzzing"""
        filename = self.get_wordlist()
        with open(filename, "r") as f:
            return f.read().strip().split("\n")


class ArgValidator:
    def __init__(self, args: list[str]):
        self.url = sys.argv[1]
        self.target = sys.argv[2]

        if PLACEHOLDER not in self.url:
            print(f"Placeholder '{PLACEHOLDER}' not found.")
            print_usage()

        if self.target not in TARGETS:
            print(
                f"Fuzzing target  '{self.target}' not supported '{TARGETS}'."
            )
            print_usage()

    def get_args(self) -> tuple[str, str]:
        """Return the URL and target"""
        return self.url, self.target


def print_usage() -> None:
    print(sys.argv)
    print(USAGE)
    exit(1)


def main():
    if len(sys.argv) != 3:
        print_usage()

    url, target = ArgValidator(sys.argv).get_args()

    fh = FileHandler(type_=target)
    fz = RequestHandler(url)

    wordlist = fh.load_wordlist()
    targets = fz.build_targets(wordlist)
    responses = fz.start_fuzz(targets)

    fm = Formatter(responses)
    fm.print_results(responses)


if __name__ == "__main__":
    main()
