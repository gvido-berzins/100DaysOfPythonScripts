---
Author: Gvido Bērziņš
Date: 03.11.2021
---

A script for searching and downloading songs from Youtube video descriptions.

## Requirements

Install the requirements.

```
pip install -r requirements.txt
```

## Usage

Print out the help menu by running the script without options or with the `-h` flag

```
$ python song-getter.py
usage: song-getter.py [-h] [--search SEARCH] [--location {newline,sameline}] url
song-getter.py: error: the following arguments are required: url
```

The script requires the target Youtube channel URL, example

```
https://www.youtube.com/c/.../videos
```

- it has to end with `/videos`

The `--search` term is meant to be an unique identifier in the description
like `Song:` which will be used as the starting point for the song link or title.

By default `newline` is set as the `--location` option, which means that the song will
be searched on the next line, but if `sameline` is supplied, then it will be taken
from the same line.

Examples:

```
$ python song-getter.py https://www.youtube.com/c/.../videos --search http:// --location sameline
$ python song-getter.py https://www.youtube.com/c/.../videos --search "Music:"
```

## How it works

The script uses Youtube-dl as it's main driver for the operations with YouTube.

1. The script creates a list of video descriptions from all channel's videos
2. Goes through each description
- If a line in the description contains the `--search` term
	- based on the `--location` value it gets the line with the song title/url
3. Goes through each song in the gathered list and parses the url
- If there is a url, it gets converted to the song title
4. Finally, using the list of song titles, all songs are downloaded
