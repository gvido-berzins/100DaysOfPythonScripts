import requests
from bs4 import BeautifulSoup as bs
import random
import os
import json
import io
from PIL import Image

base_url = 'https://xkcd.com/'
latest_endpoint = 'info.0.json'
downloads = 'xkcd/'


def save_file(id_, r):
    os.makedirs('xkcd', exist_ok=True)

    # with open(path, 'wb') as f:
        # for chunk in res.iter_content(100000):
            # f.write(chunk)
    # print(f"File saved at {path=}")
    # data = io.BytesIO(res.read())

    # b = io.BytesIO(res.content)
    # # size = 350, 350
    # img = Image.open(b)
    # # img.thumbnail(size)

    r.raw.decode_content = True # handle spurious Content-Encoding
    im = Image.open(r.raw)
    print(im.format, im.mode, im.size)
    path = downloads + f"{id_}.jpg"
    im.save(path, "JPEG")
    print(path)

    return path


def download_comic(id_):
    s = requests.session()
    url = f"{base_url}{id_}/"
    page = s.get(url).text
    soup = bs(page, 'html.parser')

    comic_url = soup.find('div', {'id': 'comic'}).find('img').get('src')
    url = base_url + comic_url
    res = s.get(url, stream=True)
    return save_file(id_, res)


def get_latest_comic_json():
    url = base_url + latest_endpoint
    return requests.get(url).json()


def err_handler(status):
    if not status:
        print("Something went wrong.")
        exit()
    else:
        print('[+] Success!')


def get_random_comic():
    latest = get_latest_comic_json()['num']
    randint = random.randint(1, latest)
    path = download_comic(randint)
    err_handler(path)
    return path


def get_latest_comic():
    latest = get_latest_comic_json()['num']
    path = download_comic(latest)
    err_handler(path)
    return path


def get_by_num(n: int):
    n = int(n)
    latest = get_latest_comic_json()['num']
    print(f'{latest=}')
    print(f'{n=}')

    if n > latest:
        print(f"Error, number larger than {latest=}")
        exit()
    elif n < 1:
        print(f"Can't go lower than {n=}")
        exit()
    else:

        path = download_comic(n)
        err_handler(path)
        return path

