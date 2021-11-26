import requests

base_url = 'https://hacker-news.firebaseio.com/v0/'
ext = '.json?print=pretty'


def build_url(stories):
    return base_url + stories + ext


def request(item, url):
    print(f"{url=}")
    if item == 'json':
        return requests.get(url).json()
    elif item == 'list':
        return [x.replace(' ','') for x in requests.get(url).text.strip().replace('[','').split(', ')]
    else:
        print(f'Unknown item {item}')


def get_top_stories(n=10):
    print('** hackernews.py **')
    story_url = build_url('topstories')
    top_stories_list = request('list', story_url)
    print(f"{top_stories_list=}")
    responses = []

    for i in range(0, n):
        url = base_url + 'item/' + top_stories_list[i] + ext

        responses.append(request('json', url))

    print(responses)
    return responses

