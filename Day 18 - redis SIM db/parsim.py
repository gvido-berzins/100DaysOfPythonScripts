#!/usr/bin/env python3

import argparse
import json
import os
import sys
from collections import defaultdict

import redis
import yaml

SCRIPT_DIR = os.path.dirname(__file__)
INPUT_DIR = os.path.join(SCRIPT_DIR, "input")
r = redis.Redis(db=15)

MODES = []
parser = argparse.ArgumentParser()
parser.add_argument(
    "command",
    help="Command",
    choices=["g", "ga", "sa", "gn", "c", "flushdb"]
)
parser.add_argument("key", nargs="*", help="For get single key")


def pretty_dict(d) -> None:
    j = json.dumps(d, indent=2)
    print("=====================================")
    print(j)
    print("=================================")


def load_file(file) -> None:
    with open(file, "r") as f:
        return vals_to_str(yaml.safe_load(f))


def check_input() -> bool:
    for file in os.listdir(INPUT_DIR):
        return True if file else False


def vals_to_str(d):
    nd = dict()

    for k, v in d.items():
        nd[k] = str(v)
    return nd


def parse_input():
    d = dict()
    for file in os.listdir(INPUT_DIR):
        path = os.path.join(INPUT_DIR, file)
        d[file] = load_file(path)

    return d


def decode_hash(h):
    d = {}
    for key, val in h.items():
        d[key.decode("utf-8")] = val.decode("utf-8")
    return d


def done():
    print("\n============")
    print("[+] DONE [+]")
    print("============")
    sys.exit(0)


def check_existing_key(key):
    s = r.exists(key)
    return s if s else False


def check_existing_hash(key, field):
    s = r.hexists(key, field)
    return s if s else False


def check_existing_hash_value(k, f, v):
    try:
        vg = r.hmget(k, f)
        match = vg[0].decode("utf-8") == v
    except AttributeError:
        return False

    return match


def print_if_exists(key, field=None, value=None, t="hash") -> None:
    """Print only existing records"""
    if t == "key":
        if check_existing_key(key):
            print(f"\n>> Key ['{key}'] exists")

    elif t == "hash":
        if check_existing_hash(key, field):
            print(f"# F: ['{key}:{field}'] exists")

    elif t == "value":
        if check_existing_hash_value(key, field, value):
            print(f"- V: ['{key}:{field}={value}'] exists")

    else:
        print("Undefined.")


def insert_all_hashed(h) -> None:
    """Insert all hashed keys"""
    with r.pipeline() as pipe:
        for key, val in h.items():
            print_if_exists(key, t="key")

            for k, v in val.items():
                if not print_if_exists(
                    key, k, t="hash"
                ) and not print_if_exists(key, k, v, t="value"):
                    pipe.hset(key, k, v)

        pipe.execute()


def insert_hash(k, f, v):
    return r.hset(k, f, v)


def get_all_keys() -> list:
    ks = sorted([k.decode("utf-8") for k in r.keys()])
    print(f"\n* All keys *\n{ks}\n")
    return ks


def get_all_data() -> defaultdict[dict]:
    """Get all data from redis"""
    d = defaultdict(dict)

    for key in get_all_keys():
        d[key].update(decode_hash(r.hgetall(key)))

    return d


def get_all_numbers_dict(d):
    num_f, pin1_f = "Number", "PIN1"
    _ = dict()

    for key, val in d.items():
        _[key] = {num_f: val[num_f], pin1_f: val[pin1_f]}
    return _


def get_hash(key):
    return {key: decode_hash(r.hgetall(key))}


def update_hash(k, f, v):
    """Update a hash record"""

    if not check_existing_hash(k, f):
        print("Field does not exist, are you sure?")

        if input("Proceed? "):
            exit("Exiting.")

    insert_hash(k, f, v)
    print("[+] Record updated.\n")
    return get_hash(k)


def main():

    if args.command == "sa":
        print(
            f"> Setting all keys from dir '{os.path.basename(INPUT_DIR)}'..."
        )

        d = parse_input()
        pretty_dict(d)
        insert_all_hashed(d)

    elif args.command == "g":
        if not args.key:
            parser.print_help()
            exit("[X] ERROR [X]\n> Provide key")

        for key in args.key:
            print(f"> Getting key {key}")
            results = get_hash(key)
            pretty_dict(results)

    elif args.command == "ga":
        print("> Getting all keys...")
        results = get_all_data()
        pretty_dict(results)

    elif args.command == "gn":
        print("> Getting numbers...")

        results = get_all_data()
        n = get_all_numbers_dict(results)
        pretty_dict(n)

    elif args.command == "c":
        """
        .py c key field value
        """
        if not args.key:
            parser.print_help()
            exit("[X] ERROR [X]\n> Provide `key field value`")

        if isinstance(args.key, list):
            key = args.key[0]
            field = args.key[1]
            value = args.key[2]
        else:
            exit("Wrong")

        print(f"> Changing key {key}")
        results = update_hash(key, field, value)
        pretty_dict(results)

    elif args.command == "flushdb":
        r.flushdb()

    else:
        print("Unsupported.")

    done()


if __name__ == "__main__":
    args = parser.parse_args()

    main()
