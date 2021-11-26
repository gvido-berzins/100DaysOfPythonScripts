import requests
import os
import json
import random
import time

boards = [
    'g', 'biz', 'diy',
    'x', 'pol', 'fit'
        ]

help_text = \
f"Get threads from the following boards {boards=}\n"\
"x number of 'lt'est threads\n"\
"x number of threads with the most 're'plies\n"\
"x number of 'r'andom threads\n"


def get_board_json(board):

    if board not in boards:
       print(f"Board not in {boards=}")
       exit()

    url = f'https://a.4cdn.org/{board}/catalog.json'
    print(f"{url=}")

    res = requests.get(url).json()
    # print(json.dumps(res, indent=2))

    return res


def assign_key(string, thread):
    key = ''
    try:
        key = thread[string]
    except KeyError:
        key = key if key else ''

    return key


def get_all_threads(json, board):
    thread_count = 0
    thread_list = []

    for el in json:
        for key, value in el.items():
            if key == 'threads':
                for thread in value:
                    time = thread['time']
                    no = thread['no']
                    com = assign_key('com', thread)
                    sub = assign_key('sub', thread)
                    replies = thread['replies']

                    thread_count += 1
                    # thread_list.append(no)

                    title = com if not sub else sub

                    thread_dict = {}
                    thread_dict = {
                            'time': time,
                            'no': no,
                            'sub': sub,
                            'com': com,
                            'replies': replies,
                            'url': f'https://boards.4channel.org/{board}/thread/{no}'
                            }

                    thread_list.append(thread_dict)
                    # print(thread_dict)

    return thread_list


def get_max_thread(thread_list, key):
    max = 0
    max_thread = {}

    for thread in thread_list:
        if thread[key] > max:
            max = thread[key]
            max_thread = thread

    return max_thread


def sort_threads_by(thread_list, key='replies'):
    return sorted(thread_list, key = lambda i: i[key], reverse=True)


def get_latest(board, n=3):
    json = get_board_json(board)
    thread_list = get_all_threads(json, board)
    latest_thread = sort_threads_by(thread_list, key='time')[:n]

    print(f"{latest_thread=}")
    return latest_thread


def get_most_popular(board, n=10):
    json = get_board_json(board)
    thread_list = get_all_threads(json, board)
    top_threads = sort_threads_by(thread_list)[:n]

    print(f"{top_threads=}")
    return top_threads


def get_random(thread_list, n):
    random_threads = []
    for i in range(0, n):
        rand = random.randint(0, len(thread_list))
        print(f"{rand=}")
        random_threads.append(thread_list[rand])

    return random_threads


def get_random_threads(board, n=1):
    json = get_board_json(board)
    thread_list = get_all_threads(json, board)
    random_threads = get_random(thread_list, n)

    print(f"{random_threads=}")
    return random_threads


# get_latest('g', n=10)
# get_most_popular('g', n=10)
# get_random_threads('g')
