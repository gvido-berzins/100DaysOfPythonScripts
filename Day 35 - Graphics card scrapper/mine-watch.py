import math
import os

import requests
from bs4 import BeautifulSoup
from pushbullet import Pushbullet

KEYWORDS = ["rx 5600xt"]  # , "RX 5700xt", "RTX 3060ti"]
KEYWORDS = ["rx 5600xt", "RX 5700xt", "RTX 3060ti"]
BASE_URL = "https://www.salidzini.lv"
SEARCH_QUERY = "/cena?q="
ITEMS_PER_PAGE = 18
NEXT_PAGE = "/&offset="

pb_api_key = os.getenv("PUSHBULLET_KEY")
pb = Pushbullet(pb_api_key)

temp_file = "note.tmp"


def compare_price():
    pass


def build_query(keyword):
    URL = BASE_URL + SEARCH_QUERY
    keyword = keyword.replace(" ", "+")
    return URL + keyword.lower()


def next_page(url, page_num):
    return url + NEXT_PAGE + str(page_num * ITEMS_PER_PAGE)


def calc_offset(total_page_num):
    return [x for x in range(1, math.ceil(total_page_num / ITEMS_PER_PAGE))]


with open(temp_file, "w") as f:
    for word in KEYWORDS:
        page = requests.get(build_query(word))
        soup = BeautifulSoup(page.text, "html.parser")
        # print(soup)

        try:
            total_results = int(
                soup.find("span", itemprop="numberOfItems").text)
        except:
            print("Error: Are you a robot?")

            f.write(f"{soup}")
            break

        print(f"\n> Looking for {word}")
        for p in calc_offset(total_results):
            page = requests.get(next_page(build_query(word), p))
            # print(next_page(build_query(word),p))
            soup = BeautifulSoup(page.text, "html.parser")

            item_box = soup.find_all(class_="item_box_main")

            for x in item_box:
                item_stock = x.find(class_="item_stock")
                item_name = x.find(class_="item_name")
                item_price = x.find("span").text
                link = BASE_URL + x.find(class_="item_link", href=True)["href"]
                if not item_stock.find("span") and "Reklāma" not in x.text:
                    print(
                        f"{item_name.text}\n{item_price} - {item_stock.text}\n{link}\n"
                    )
                # print(x.select('.item_stock > span'))

with open(temp_file, "r") as f:
    note = f.readlines()

note = "".join(str(e) for e in note)
pb.push_note("> Here are your finds sir:", note)
os.remove(temp_file)
