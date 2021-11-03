#!/usr/bin/env python

import argparse
import youtube_dl
import json
import re


SONG_REGEX = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
DEFAULT_OPTS = {
    # 'format': 'bestaudio/best',
    'writedescription': True,
    'outtmpl': '%(uploader)s/%(title)s.%(ext)s',
}


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('url')
    # parser.add_argument('--download', action="store_true", default=False)
    parser.add_argument('--search', default="Song", help="Search term")
    parser.add_argument(
        '--location',
        default="newline",
        choices=["newline", "sameline"],
        help="Song URL or title location"
    )
    return parser.parse_args()


class YoutubeDL:
    """Class representing a Youtube-dl Object"""
    def __init__(self):
        self.ydl = youtube_dl.YoutubeDL(DEFAULT_OPTS)

    def get_video_info(self, url):
        """Returns a json string which contains all video info"""
        return self.ydl.extract_info(url, download=False)

    def download_by_title(self, url_list, opts):
        ydl = youtube_dl.YoutubeDL(opts)
        res = ydl.download(url_list)


def get_all_descriptions(video_list):
    return [item['description'] for item in video_list['entries']]


def jp(data):
    pdata = json.dumps(data, indent=2)
    print(pdata)
    return pdata


def download_handler(url):
    ytdl = YoutubeDL()

    if 'videos' in url.split('/'):
        print("> Downloading all of the channel's videos.")

    video_list = ytdl.get_video_info(url)
    return video_list


def process_description(description):
    return description.split("\n")


def find_all_songs(descriptions, to_search, location):
    song_list = []
    for description in descriptions:
        description = process_description(description)
        song = find_song(description, to_search, location)

        if song:
            song_list.append(song)
            print(song)

    return song_list


def find_song(description, to_search, location):
    found_list = []

    for i, line in enumerate(description):
        if to_search in line:
            if location == "newline":
                found_list.append(description[i+1])

            if location == "sameline":
                found_list.append(line.split(to_search)[-1])

    try:
        return found_list[0]
    except IndexError:
        return None


def parse_found_urls(all_songs):
    for i, line in enumerate(all_songs):
        m = re.search(SONG_REGEX, line)
        if m:
            all_songs[i] = m.group(1)

    return all_songs


def get_video_titles(links):
    ytdl = YoutubeDL()
    for i, link in enumerate(links):
        if re.search(SONG_REGEX, link):
            video_info = ytdl.get_video_info(link)
            title = video_info.get('title')
            links[i] = title

    return links


def download_all_songs_by_title(url_list, opts=None):
    """Download all songs by title"""

    if not opts:
        opts = {
            'format': 'm4a',
            'extract_audio': True,
            'default_search': 'ytsearch',
            'outtmpl': 'downloads/%(title)s.%(ext)s',
            'ignoreerrors': True,
        }

    ydl = YoutubeDL()
    ydl.download_by_title(url_list, opts)


def main():
    video_list = download_handler(args.url)
    descriptions = get_all_descriptions(video_list)
    all_songs = find_all_songs(descriptions, args.search, args.location)
    all_songs_parsed = parse_found_urls(all_songs)
    all_titles = get_video_titles(all_songs_parsed)
    print("\n\nSongs to download.")
    jp(all_titles)

    print("\n\nDownload started.")
    download_all_songs_by_title(all_titles)

    print("================")
    print("+++++ DONE +++++")
    print("================")


if __name__ == "__main__":
    args = parse_args()
    main()
