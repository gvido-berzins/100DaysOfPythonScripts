import argparse
import json
import os
import re

import requests
from dotenv import load_dotenv

load_dotenv()
API_ID = os.getenv("API_ID")
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
JWT = os.getenv("JWT")
TO_NUMBER = os.getenv("TO_NUMBER")
FROM_NUMBER = os.getenv("FROM_NUMBER")
SERVER_URL = os.getenv("SERVER_URL")

MESSAGE_TYPES = ["text", "media"]
MESSAGES_URL = "https://messages-sandbox.nexmo.com/v0.1/messages"

# https://gist.github.com/gruber/249502
URL_REGEX = r'(?i)\b((?:[a-z][\w-]+:(?:/{1,3}|[a-z0-9%])|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?«»“”‘’\]))"\'`]))'

DEFAULT_HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json"
}
FROM_DICT = {"type": "whatsapp", "number": FROM_NUMBER}
TO_DICT = {"type": "whatsapp", "number": TO_NUMBER}

AUDIO_EXT = ["aac", "mp3", "amr", "mpeg", "opus", "ogg"]
VIDEO_EXT = ["mp4", "3gpp"]
IMAGE_EXT = ["png", "jpg", "jpeg"]


def parse_args():
    parser = argparse.ArgumentParser(
        description="CLI WhatsApp API manager"
    )
    parser.add_argument("-t", "--text", help="The message to send")
    parser.add_argument(
        "-m",
        "--media",
        help="Link to the object, can be an filepath or a remote link"
    )
    parser.add_argument(
        "-c",
        "--caption",
        help="Caption for the media message",
        default=""
    )
    return parser.parse_args()


def detect_url(url):
    """Check if the give link is the URL"""
    return True if re.search(URL_REGEX, url) else False


def send_message(message):
    """Send a simple WhatsApp message"""
    data = {
        "from": FROM_DICT,
        "to": TO_DICT,
        "message": {
            "content": {
                "type": "text",
                "text": message
            }
        },
    }
    data = json.dumps(data)
    r = requests.post(
        url=MESSAGES_URL,
        headers=get_headers("text"),
        data=data,
        auth=(API_KEY, API_SECRET),
    )
    print("> Message sent.")
    print(r)
    print(r.text)


def get_media_headers():
    headers = {"Authorization": f"Bearer {JWT}"}
    return DEFAULT_HEADERS | headers


def get_text_headers():
    return DEFAULT_HEADERS


def get_headers(type_):
    """Get the right headers based on the message type"""
    if type_ == "media":
        headers = get_media_headers()
        return json_parse_headers(headers)

    if type_ == "text":
        headers = get_text_headers()
        return json_parse_headers(headers)

    return json_parse_headers(headers)


def json_parse_headers(headers):
    return json.loads(json.dumps(headers))


def send_media(url, type_, caption):
    """Send a WhatsApp media message"""
    type_ = detect_message_type(url)
    data = {
        "from": FROM_DICT,
        "to": TO_DICT,
        "message": {
            "content": {
                "type": type_,
                type_: {
                    "url": url,
                    "caption": caption
                }
            }
        },
    }
    data = json.dumps(data)
    r = requests.post(
        MESSAGES_URL, headers=get_headers("media"), data=data
    )
    print("> Message sent.")
    print(r)
    print(r.text)


def detect_message_type(url):
    """Detect the message type based on the extension in the link

    Supported types can be seen here:
    - https://developers.facebook.com/docs/whatsapp/api/media/"""
    ext = url.split(".")[-1]

    if ext in AUDIO_EXT:
        return "audio"

    if ext in VIDEO_EXT:
        return "video"

    if ext in IMAGE_EXT:
        return "image"

    return "document"


def main():
    """To test the curl commands in Python data payloads, this can be used
    - https://curlconverter.com/"""
    if not args.text and not args.media:
        print(
            "Nothing specified, please specifiy the message or media flags"
        )
        exit(1)

    if args.text:
        print("> Sending a TEXT message.")
        send_message(args.text)
        exit()

    url = args.media
    caption = args.caption
    is_remote = detect_url(url)
    is_gif = url.endswith(".gif")
    media_type = detect_message_type(url)

    print("> Sending a MEDIA message.")

    if is_gif:
        print("Sending a link of a gif (not supported in WhatsApp API)")
        send_message(url)
        exit()

    send_media(url, media_type, caption)


if __name__ == "__main__":
    args = parse_args()
    main()
