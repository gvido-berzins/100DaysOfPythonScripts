import asyncio
import os
import time

import requests
from bs4 import BeautifulSoup
from bs4 import BeautifulSoup as bs
from colorama import Fore

SCRIPT_DIR = os.path.dirname(__file__)
DOWNLOADS_DIR = os.path.join(SCRIPT_DIR, "downloads")
DEFAULT_PAGE_DUMP_FILENAME = "page-dump.html"

PROJECT_AWESOME_URL = "https://project-awesome.org/unixorn/awesome-zsh-plugins#themes"
GITHUB_URL = "https://github.com"
RAW_TRUE = "?raw=true"
RAW_GITHUB_CONTENT = "https://raw.githubusercontent.com/"

ZSH_THEME_SELECTOR = "h2#themes+p+ul>li>a[href]:first-of-type"
EXTENSIONS = ["png", "jpg", "jpeg", "gif"]
TAGS = ["a", "img"]
ATTRIBUTES = ["data-canonical-src", "href"]
GITHUB_REPOSITORY_IMAGE_SELECTOR = ", ".join(
    [
        f'.repository-content {tag}[{attr}*="{ext}" i]' for tag in TAGS
        for attr in ATTRIBUTES for ext in EXTENSIONS
    ]
)


def term_print(text: str, color: str = "reset", end="\n") -> None:
    """Pretty print terminal text by providing color names"""
    print(
        Fore.__dict__.get(color.upper(), Fore.RESET) + text + Fore.RESET,
        end=end
    )


def dump_page(page: str, filename=DEFAULT_PAGE_DUMP_FILENAME) -> None:
    """Dump the page for later reuse"""
    with open(filename, "w") as f:
        f.write(page)


def load_page(filename=DEFAULT_PAGE_DUMP_FILENAME) -> str:
    """Dump the page for later reuse"""
    with open(filename, "r") as f:
        return f.read()


async def get_request(url: str, timeout: int = 10) -> str:
    """Send a get request and return the text of the response"""
    return requests.get(url, timeout=timeout)


async def get_page(url: str, initial: bool = True) -> str:
    """Get the HTML page from an HTTP response text"""
    html = ""
    if os.path.isfile(DEFAULT_PAGE_DUMP_FILENAME) and initial:
        html = load_page()
    else:
        html = await get_request(url)
        html = html.text

    return bs(html, "html.parser")


def get_all_theme_urls(page: BeautifulSoup) -> list[str]:
    """Get all theme URLs by using a CSS selector"""
    return [
        el.get("href").rstrip("/")
        for el in page.select(ZSH_THEME_SELECTOR)
    ]


async def get_all_screenshot_urls(page: BeautifulSoup) -> list[str]:
    """Get all screenshot URLs by using a CSS selector"""
    url_list = []
    for el in page.select(GITHUB_REPOSITORY_IMAGE_SELECTOR):
        url = list(
            filter(None, [el.get("data-canonical-src"),
                          el.get("href")])
        )
        try:
            url = url[0]
        except IndexError:
            pass

        url = url.rstrip("/")

        if not url.startswith("http"):
            url = RAW_GITHUB_CONTENT + url.replace("/blob/", "/")
        elif url.startswith(GITHUB_URL):
            url = url.replace("/blob/",
                              "/").replace(GITHUB_URL, RAW_GITHUB_CONTENT)

        url = url.replace(RAW_TRUE, "")

        url_list.append(url)
    return url_list


def request_url(url: str, timeout: int = 70) -> requests.Request:
    try:
        return requests.get(url, timeout=timeout)
    except requests.exceptions.ConnectionError:
        term_print("Probably quota. Sleeping {timeout} seconds", "red")
        time.sleep(timeout)


async def save_screenshots(folder_name: str, urls: list[str]) -> None:
    """Donwload the screenshot and save in a directory"""
    abs_folder_path = os.path.join(DOWNLOADS_DIR, folder_name)

    for url in urls:
        term_print(f"Screenshot URL:", "LIGHTCYAN_EX", end=" ")
        term_print(f"{url}", "LIGHTRED_EX")
        path = os.path.join(abs_folder_path, os.path.basename(url))
        if os.path.isfile(path):
            print_skip("Screenshot already downloaded.")
            continue
        os.makedirs(abs_folder_path, exist_ok=True)
        image_content = await get_request(url)

        with open(path, "wb") as f:
            for chunk in image_content.iter_content(100000):
                f.write(chunk)


async def save_all_screenshots_from_url(url: list[str], timeout=0) -> None:
    """Visit all GitHub pages and get the screenshots"""
    time.sleep(timeout)
    title = os.path.basename(url)
    page = await get_page(url, initial=False)
    screenshot_urls = await get_all_screenshot_urls(page)
    print(
        f"\n=> {Fore.WHITE}THEME Repository: {Fore.MAGENTA}'{url}'{Fore.LIGHTWHITE_EX}: {Fore.LIGHTMAGENTA_EX}'{title}'",
        Fore.RESET,
    )
    term_print("URL count:", "yellow", end=" ")
    term_print(f"{len(screenshot_urls)}", "LIGHTYELLOW_EX")

    if RAW_GITHUB_CONTENT in url:
        print_skip("Raw content")
        return
    await save_screenshots(folder_name=title, urls=screenshot_urls)


def print_skip(reason):
    term_print(f"{reason}, skipping.", "gray")


async def main():
    page = await get_page(PROJECT_AWESOME_URL)
    urls = get_all_theme_urls(page)
    tasks = [save_all_screenshots_from_url(x) for x in urls]
    asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())
