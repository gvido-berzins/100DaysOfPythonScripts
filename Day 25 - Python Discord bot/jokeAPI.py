import requests

base_url = "https://v2.jokeapi.dev/joke/"
filters = "Programming,Miscellaneous,Dark,Pun,Spooky?blacklistFlags=nsfw,racist,sexist&format=txt&type=single"
url = base_url + filters

help_text = f"Get a joke from jokeAPI\nEndpoint: {url}"

def get_joke():
    return requests.get(url).text

