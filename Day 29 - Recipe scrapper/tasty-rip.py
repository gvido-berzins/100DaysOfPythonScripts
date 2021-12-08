import os
import sys

import requests
from bs4 import BeautifulSoup
from pushbullet import Pushbullet

pb = Pushbullet(os.getenv("PUSHBULLET_API_KEY"))

url = sys.argv[1]
page = requests.get(url)
soup = BeautifulSoup(page.text, "html.parser")
temp_file = "note.tmp"
ingredients = soup.find_all(class_="ingredients")

with open(temp_file, "w") as f:
    for ing in ingredients:
        f.write("# Ingeredients: \n")
        ing_row = ing.find_all(class_="ing-list-item")
        for i in ing_row:
            amount = (i.find(class_="ing-amount").text.strip()
                      if i.find(class_="ing-amount") != None else "")

            ingredient = i.find("u").text if i.find("u") is not None else ""
            f.write(f"+ {ingredient} [{amount}]\n")

    start = False
    f.write("\n# Instructions: \n")
    article = soup.find(class_="article-body-content")

    i = 1
    for s in article.find_all("p"):
        if s.find(class_="recipe-list-start"):
            start = True
        if s.find(class_="recipe-list-end"):
            start = False
        if start and s.text != "":
            f.write(f"## {i}.\n{s.text}\n")
            i += 1

with open(temp_file, "r") as f:
    note = f.readlines()

title = soup.find(class_="article-title").text.strip()
note = "".join(str(e) for e in note)

pb.push_note(title, note)
os.remove(temp_file)
