import ast
import json
import os
import subprocess
import time

import requests

SCRIPT_DIR = os.path.dirname(__file__)
LOG_DIR = os.path.join(SCRIPT_DIR, "logs")
HASH_FILE = os.path.join(LOG_DIR, "hashes.log")
LOG_FILE = os.path.join(LOG_DIR, "log.log")

XMR = "XMRWALLET"
URL = f"https://api.moneroocean.stream/miner/{XMR}/stats/"

HASH_TOLERANCE = 7000.00


class GMiner:
    def __init__(self):
        self.wallet_id = "0x01ETHWALLET"
        self.url = "https://eth.2miners.com"
        self.accounts = "/api/accounts/"
        self.stats = ""

    def get_stats(self):
        request = f"{self.url}{self.accounts}{self.wallet_id}"
        self.stats = requests.get(request).json()

    def get_active(self):
        return True if self.stats["workersOnline"] == 1 else False


def write_to(file, data):
    with open(file, "w") as f:
        f.write(f"{data}")


def append_to(file, data):
    with open(file, "a") as f:
        f.write(f"{data}\n")


def read_file(file):
    with open(file, "r") as f:
        return [x for x in f.read().split("\n") if x != ""]


def json_write(file, data):
    with open(file, "w") as f:
        f.write(json.dumps(data))


def json_read(file):
    with open(file, "r") as f:
        return ast.literal_eval(f.read())


def next_log_number():
    numbers = [
        f.split("-")[0] for f in os.listdir("logs/")
        if f != "hashes.log" and f != "log.log"
    ]
    return max(list(map(lambda x: int(x), numbers))) + 1 if numbers else 0


def log(message):
    timestamp = time.strftime("%Y-%m-%d-%H:%M:%S")
    message = f"[{timestamp}] '{message}'"
    append_to(LOG_FILE, message)


def main():
    sleep_time = 30
    gminer = GMiner()

    while True:
        try:
            # First check gminer status
            gminer.get_stats()
            gminer_active = gminer.get_active()

            if not gminer_active:
                cmd = f"notify-send -u critical 'GMiner is offline!'"
                log(cmd)
                subprocess.check_output(cmd, shell=True)

            # Finally check monero rig
            response = requests.get(URL)

            file = os.path.join(
                LOG_DIR, f"{next_log_number()}-response.json"
            )
            json_write(file, response.json())  # Log the response

            hash_ = json_read(file)["hash"]
            append_to(HASH_FILE, hash_)
            latest_hash = float(read_file(HASH_FILE)[-1])

            if latest_hash < HASH_TOLERANCE:
                cmd = f"notify-send -u critical 'Moneroocean hashrate report is low - {latest_hash}'"
                log(cmd)
                subprocess.check_output(cmd, shell=True)

        except Exception as e:
            print(e)
            log(e)
            continue

        time.sleep(sleep_time)


if __name__ == "__main__":
    main()
