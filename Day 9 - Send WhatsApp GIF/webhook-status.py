#!/usr/bin/env python3

from pprint import pprint
from flask import Flask, request

app = Flask(__name__)


@app.route("/webhooks/message-status", methods=["POST"])
def message_status():
    data = request.get_json()
    pprint(data)
    return "200"


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=9003, debug=True)
