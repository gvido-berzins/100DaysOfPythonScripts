import csv
import os
import subprocess
import sys
import time
import traceback

import pyperclip
import requests
from bs4 import BeautifulSoup

base_url = "https://tokensniffer.com"
new_tokens_url = base_url + "/tokens/new"
# new_tokens_url = 'https://tokenfomo.io/'

output_file = "tokens.csv"
LOG_FILE = "token.log"


def to_csv(rows, filename=output_file):
    with open(filename, "w") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(rows)


def read_csv(filename=output_file):
    data = []
    with open(filename, newline="") as csvfile:
        rows = csv.reader(csvfile, delimiter=",", quotechar="|")
        # return ["".join(row) for row in rows]
        return [row for row in rows]


def get_table_rows(soup):
    table = soup.find("table")
    output_rows = []
    for table_row in table.findAll("tr"):
        headers = table_row.findAll("th")
        columns = table_row.findAll("td")
        output_row = []

        for header in headers:
            output_row.append(header.text)
            output_row.append(header.find("a").get("href"))

        for column in columns:
            output_row.append(column.text)

        output_rows.append(output_row)

    return output_rows


def append_to(data, file=LOG_FILE):
    with open(file, "a") as f:
        f.write(f"{data}\n")


def log(message):
    timestamp = time.strftime("%Y-%m-%d-%H:%M:%S")
    message = f"[{timestamp}] '{message}'"
    append_to(message)


def main():

    while True:

        try:
            data = requests.get(new_tokens_url,
                                headers={"User-Agent": "Mozilla/5.0"})
            soup = BeautifulSoup(data.text, "html.parser")
            new_token = get_table_rows(soup)

            if not os.path.isfile(output_file):
                to_csv(new_token)

            prev_token = read_csv()
            to_csv(new_token)

            new_token = new_token[0]
            prev_token = prev_token[0]
            print(new_token[0], prev_token[0])

            if new_token[0] != prev_token[0]:

                cmd = f'notify-send -u critical "New! {new_token}"'
                log(new_token)
                subprocess.check_output(cmd, shell=True)
                pyperclip.copy(base_url + new_token[1])
        except Exception:
            traceback.print_exc(file=sys.stdout)
        time.sleep(30)


if __name__ == "__main__":
    main()
