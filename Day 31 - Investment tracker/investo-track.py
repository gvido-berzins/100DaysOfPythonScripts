import datetime
import json
import logging
import os
import time

SCRIPT_DIR = os.path.dirname(__file__)
log_file = os.path.join(SCRIPT_DIR, "track.log")

logging.basicConfig(
    filename=log_file,
    format="%(levelname)s:%(message)s",
    encoding="utf-8",
    level=logging.DEBUG,
)

track_filename = "track.json"
json_file = os.path.join(SCRIPT_DIR, track_filename)

currencies = ["EUR", "USD", "USDT", "SAI"]
actions = ["BUY", "SELL"]


def corrector(input_, list_):
    while True:
        output = input(input_).upper()
        if output in list_:
            break
        else:
            print("Incorrect option. Try:", list_)
    return output


def write_json(data, filename=json_file):
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)


try:
    investment = input("Investment: ").upper()
    price = input("Price per investment: ")
    action = corrector("Buy/Sell: ", actions)
    amount = input("Amount: ")
    currency = corrector("Currency: ", currencies)
    fee = input("Fee: ")
    fee_currency = corrector("Fee currency: ", currencies)

    ts = time.time()
    timestamp = datetime.datetime.fromtimestamp(ts).strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    logging.info(
        f"Adding entry: {investment}, {price}, {currency}, {action}, {amount}, {fee}, {fee_currency} --> '{track_filename}'"
    )

    entry = {
        "investment": investment,
        "price": price,
        "currency": currency,
        "action": action,
        "amount": amount,
        "fee": fee,
        "fee_currency": fee_currency,
        "timestamp": timestamp,
    }

    logging.info(f"Opening: {track_filename}")

    with open(json_file) as f:
        logging.info(f"Loading: {track_filename}")
        data = json.load(f)
        temp = data["trades"]

        logging.info(f"Appending to: {track_filename}")
        temp.append(entry)

    write_json(data)
    logging.info(
        f"New entry added: {investment}, {currency}, {action}, {amount}, {fee}, {fee_currency} --> '{json_file}'"
    )

except Exception as e:
    print(f"Exception caught: {e}")
    logging.ERROR(f"{e}")
