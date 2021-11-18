import asyncio
import os
import time

import requests
from bs4 import BeautifulSoup
from bs4 import BeautifulSoup as bs

DEFAULT_PAGE_DUMP_FILENAME = "page-dump.html"
PROJECT_AWESOME_URL = "https://project-awesome.org/unixorn/awesome-zsh-plugins#themes"
GITHUB_URL = "https://github.com"
RAW_GITHUB_CONTENT = "https://raw.githubusercontent.com/"
SCRIPT_DIR = os.path.dirname(__file__)
DOWNLOADS_DIR = os.path.join(SCRIPT_DIR, "downloads")

ZSH_THEME_SELECTOR = "h2#themes+p+ul>li>a[href]:first-of-type"
GITHUB_REPOSITORY_IMAGE_SELECTOR = '.repository-content a[href*="png" i]'


def dump_page(page: str, filename=DEFAULT_PAGE_DUMP_FILENAME) -> None:
    """Dump the page for later reuse"""
    with open(filename, "w") as f:
        f.write(page)


def load_page(filename=DEFAULT_PAGE_DUMP_FILENAME) -> str:
    """Dump the page for later reuse"""
    with open(filename, "r") as f:
        return f.read()


async def send_request(url: str) -> str:
    """Send a get request and return the text of the response"""
    return await requests.get(url).text


def get_page(url: str, initial: bool = True) -> str:
    """Get the HTML page from an HTTP response text"""
    html = ""
    if os.path.isfile(DEFAULT_PAGE_DUMP_FILENAME) and initial:
        html = load_page()
    else:
        html = send_request(url)

    return bs(html, "html.parser")


async def get_all_theme_urls(page: BeautifulSoup) -> list[str]:
    """Get all theme URLs by using a CSS selector"""
    return [
        el.get("href").rstrip("/")
        for el in page.select(ZSH_THEME_SELECTOR)
    ]


def get_all_screenshot_urls(page: BeautifulSoup) -> list[str]:
    """Get all screenshot URLs by using a CSS selector"""
    url_list = []
    for el in page.select(GITHUB_REPOSITORY_IMAGE_SELECTOR):
        url = el.get("href").rstrip("/")
        if not url.startswith("http"):
            url = RAW_GITHUB_CONTENT + url.replace("/blob/", "/")
        elif url.startswith(GITHUB_URL):
            url = url.replace("/blob/",
                              "/").replace(GITHUB_URL, RAW_GITHUB_CONTENT)
        url_list.append(url)
    return url_list


async def save_screenshots(folder_name: str, urls: list[str]) -> None:
    """Donwload the screenshot and save in a directory"""
    abs_folder_path = await os.path.join(DOWNLOADS_DIR, folder_name)

    for url in urls:
        print(f"Screenshot URL: {url}")
        path = await os.path.join(abs_folder_path, os.path.basename(url))
        await os.makedirs(abs_folder_path, exist_ok=True)
        image_content = await requests.get(url)

        with open(path, "wb") as f:
            for chunk in image_content.iter_content(100000):
                f.write(chunk)


async def save_all_screenshots_from_urls(
    urls: list[str], timeout=0
) -> None:
    """Visit all GitHub pages and get the screenshots"""
    for url in urls:
        time.sleep(timeout)
        title = await os.path.basename(url)
        page = get_page(url, initial=False)
        print(f"THEME Repository: '{url}'")
        print(f"title: '{title}'")
        screenshot_urls = await get_all_screenshot_urls(page)
        print(screenshot_urls)
        save_screenshots(folder_name=title, urls=screenshot_urls)


async def main():
    page = get_page(PROJECT_AWESOME_URL)
    urls = await get_all_theme_urls(page)
    commands = [
        asyncio.ensure_future(
            x for x in
            save_all_screenshots_from_urls(urls[11:14], timeout=0)
        )
    ]
    asyncio.gather(*urls)


if __name__ == "__main__":
    asyncio.run(main())
