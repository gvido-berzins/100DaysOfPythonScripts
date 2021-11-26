import json
import urllib.parse
import requests

base_url = "http://8ball.delegator.com"
path = "/magic/JSON/"
url = base_url + path

help_text = "Ask the magic 8-ball something."

def ask_8ball(q):
    q = urllib.parse.quote(q)
    return requests.get(url + q).json()['magic']['answer']
