import requests

base_url = "https://evilinsult.com/"
filters = "generate_insult.php?lang=en&type=text"
url = base_url + filters

help_text = f"Insult someone, for fun ofcourse :)\nEndpoint: {url}"


def get_insult():
    return requests.get(url).text

