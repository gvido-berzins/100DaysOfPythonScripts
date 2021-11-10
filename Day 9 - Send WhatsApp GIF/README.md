---
Author: Gvido Bērziņš
Date: 10.11.2021
---

WhatsAppAPI messenger, send messages, videos, images to your WhatsApp.

## Prerequisites

Vonage account and an app configured there.

```
pip install -r requirements.txt
```

## Usage

Run the script with either `-m` for media or `-t` for a plain message.

```
$ python wpp_send.py -h
usage: wpp_send.py [-h] [-t TEXT] [-m MEDIA] [-c CAPTION]

CLI WhatsApp API manager

optional arguments:
  -h, --help            show this help message and exit
  -t TEXT, --text TEXT  The message to send
  -m MEDIA, --media MEDIA
                        Link to the object, can be an filepath or a remote link
  -c CAPTION, --caption CAPTION
                        Caption for the media message
```

## Examples

Sending media

```
python wpp_send.py -m https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/WhatCarCanYouGetForAGrand.mp4
```

Sending messages

```
python wpp_send.py "Message from Python!"
```

Sending a GIF link

```
python wpp_send.py -m http://11.11.111.110/hello.gif
```

## Note

This was supposed to be a GIF sender, but it turns out WhatsApp doesn't support GIFs with its API, I was bummed, because whenever I wanted to send a GIF through WhatsApp, I would not be able to, I needed to do it through sending the GIF to my phone and then sending it from my phone.

I wanted to also add a converter afterwards for webms, if I want to send a webm as a GIF, it's converted to GIF, send to a webserver directory and finally the link sent to my WhatsApp.
