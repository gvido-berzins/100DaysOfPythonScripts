import os
from dataclasses import dataclass, field

import mutagen
from tqdm import tqdm

SONG_DIR = "/path/to/music"  # CHANGE THIS

# soulseek_downloads = 'link/from/config'
ORGANIZED_DIR = os.path.join(SONG_DIR, "organized")
UNSORTED_DIRNAME = "unsorted"
EXTENSIONS = ("opus", "mp3", "m4a", "flac", "ogg", "wav", "avi")
KNOWN_TITLE = ["title", "Title", "©nam", "TIT1", "TIT2"]
KNOWN_ALBUM = ["album", "Album", "©alb", "TALB"]
KNOWN_ARTIST = ["artist", "Artist", "©ART", "aART", "TPE1", "TPE2"]


@dataclass
class SongData:
    """Data class representing the song to be organized."""

    path: str
    title: str = field(default="")
    artist: str = field(default="")
    album: str = field(default="")


def spider_dirs() -> list[str]:
    """Recursively search directories for files that end with the defined
    file extensions.
    """
    return [
        os.path.join(dp, f) for dp, dn, fn in tqdm(os.walk(SONG_DIR))
        for f in fn if f.endswith(EXTENSIONS)
    ]


def get_metadata_using_a_list(
    path: mutagen.File, keywords: list[str]
) -> str:
    """Get the metadata from a path using a mutagen File class with known keywords"""
    song_data = mutagen.File(path)
    for keyword in keywords:
        try:
            metadata = song_data.get(keyword, None)
            if metadata:
                return metadata

        except ValueError:
            pass

    return ""


def extract_metadata(file_list: list[str]) -> list[SongData]:
    """Extract metadata from all given songs paths"""
    return [
        SongData(
            path=path,
            title=get_metadata_using_a_list(path, KNOWN_TITLE),
            artist=get_metadata_using_a_list(path, KNOWN_ARTIST),
            album=get_metadata_using_a_list(path, KNOWN_ALBUM),
        ) for path in tqdm(file_list)
    ]


def make_destination_path(song: SongData) -> str:
    """Make the destination path as in path and location on disk"""
    basename = os.path.basename(song.path)
    # TODO: Fix this mess
    try:
        destination = os.path.join(ORGANIZED_DIR, song.artist, song.album)
    except TypeError:
        try:
            song.album = song.album.text
        except AttributeError:
            pass
        try:
            song.artist = song.artist.text
        except AttributeError:
            pass

        if isinstance(song.artist, list):
            if bool(song.artist):
                song.artist = song.artist[0]
            else:
                song.artist = ""

        if isinstance(song.album, list):
            if bool(song.album):
                song.album = song.album[0]
            else:
                song.album = ""

        try:
            destination = os.path.join(
                ORGANIZED_DIR, song.artist, song.album
            )
        except:
            breakpoint()

    if destination == ORGANIZED_DIR:
        destination = os.path.join(destination, UNSORTED_DIRNAME)

    os.makedirs(destination, exist_ok=True)
    return os.path.join(destination, basename)


def organize_songs_by_metadata(song_list: list[SongData]) -> None:
    """Organize the songs by a pre-defined structure"""
    for song in tqdm(song_list):
        os.rename(song.path, make_destination_path(song))


def main():
    print("🕷 Starting spider 🕷")
    print("-------------------")
    file_list = spider_dirs()

    print("⛏️ Extracting metadata ⛏️")
    print("-------------------------")
    extracted_metadata = extract_metadata(file_list)

    print("🧹 Organizing data 🧹")
    print("---------------------")
    organize_songs_by_metadata(extracted_metadata)
    breakpoint()

    print("✅ DONE ✅")


if __name__ == "__main__":
    main()
    """ TODO
        - Clean-up empty directies
        - Fallback to getting metadata from the filename
        - Make it async
    """
