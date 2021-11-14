#!/usr/bin/env python3

import json
import os
import traceback

import spotipy
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth

SCRIPT_DIR = os.path.dirname(__file__)
DOWNLOAD_DIR = os.path.join(SCRIPT_DIR, "downloads")
load_dotenv()


class SpotifyAPI:
    """Class representing the Spotify API"""
    def __init__(self, scope="user-library-read"):
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))


class User(SpotifyAPI):
    """Class representing the User of the SpotifyAPI"""
    def __init__(self, scope="user-library-read"):
        super().__init__(scope=scope)
        self.user_info = dict()
        self.playlists = None
        self.saved_tracks = None
        self.saved_albums = None

    def load_playlists(self, limit=50, offset=0):
        """Load all users playlists"""
        self.playlists = self.sp.current_user_playlists(
            limit=limit, offset=offset
        )

    def load_saved_tracks(self, limit=20, offset=0):
        """Load all saved tracks"""
        self.saved_tracks = self.sp.current_user_saved_tracks(
            limit=limit, offset=offset
        )

    def load_saved_albums(self, limit=20, offset=0):
        """Load all saved albums"""
        self.saved_albums = self.sp.current_user_saved_albums(
            limit=limit, offset=offset
        )


def print_json(j) -> str:
    """Pretty print JSON string"""
    j = json.dumps(j, indent=2)
    print(j)


def get_links(category: str, responses: list):
    """Get the song links from spotify API JSON response"""
    link_list = []
    for item in responses:
        try:
            if category == "playlist":
                link_list.append(
                    [item["name"], item["external_urls"]["spotify"]]
                )
            elif category == "album":
                item = item["album"]
                link_list.append(
                    [item["name"], item["external_urls"]["spotify"]]
                )
            elif category == "track":
                item = item["track"]
                link_list.append(
                    [item["name"], item["external_urls"]["spotify"]]
                )

        except:
            traceback.print_exc()

    return link_list


def craft_command(url: str, download_path: str) -> str:
    """Craft a command with arguments to execute"""
    return f"spotify_dl -l '{url}' -o '{download_path}' -s yes -m"


def download_songs_from_spotify(queue: dict) -> None:
    """Download songs using `spotify_dl` system command"""
    for categories, song_links in queue.items():
        for link in song_links:
            r, url = link
            download_path = os.path.join(DOWNLOAD_DIR, categories)
            command = craft_command(url, download_path)
            status = os.system(command)
            print(download_path, command)
            print(status)


def main():
    spa = User()
    spa.load_saved_tracks(limit=25)
    spa.load_saved_albums(limit=25)
    spa.load_playlists(limit=25)

    playlists, tracks, albums = spa.playlists, spa.saved_tracks, spa.saved_albums
    playlists = get_links("playlist", playlists["items"])
    tracks = get_links("track", tracks["items"])
    albums = get_links("album", albums["items"])

    download_queue = {
        "playlists": playlists,
        "tracks": tracks,
        "albums": albums,
    }

    print_json(download_queue)
    download_songs_from_spotify(download_queue)


if __name__ == "__main__":
    main()
