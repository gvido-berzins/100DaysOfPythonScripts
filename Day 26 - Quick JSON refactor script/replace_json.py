import json
from copy import copy
from glob import glob
from json import JSONEncoder
from uuid import uuid4

src = "/source/"


class MarkedList:
    """Class for marking a list to create prettier output"""

    _list = None

    def __init__(self, lst):
        self._list = lst


class CustomJSONEncoder(JSONEncoder):
    """Custom encoder for encoding a list as a string so it can be pretty printed"""
    def default(self, o):
        if isinstance(o, MarkedList):
            return "##<{}>##".format(o._list).replace("'", '"')


def parse_json(data: dict):
    """Pretty parse JSON lists"""
    b = json.dumps(
        data, indent=2, separators=(",", ": "), cls=CustomJSONEncoder
    )
    b = b.replace('"##<', "").replace('>##"', "").replace('\\"', '"')
    return b


def get_all_configs() -> list[str]:
    """Get all configuration files with glob"""
    return glob(src + "**/file.json", recursive=True)


def load_json(filename: str) -> dict:
    with open(filename, "r") as f:
        return json.load(f)


def dump_json(filename: str, data: str) -> None:
    with open(filename, "w") as f:
        f.write(data)


def jp(p: dict) -> None:
    j = parse_json(p)
    print(j)


def replace_source(config, source_name: str) -> dict:
    """Replace all source keys with given"""

    for pi, profile in enumerate(config["profiles"]):
        config["profiles"][pi]["id"] = str(uuid4())
        config["profiles"][pi]["sink"]["id"] = str(uuid4())

        for si, source in enumerate(profile["key_source"]):
            if source["type"] == source_name:
                new_source = copy(source)

                new_source["id"] = str(uuid4())
                new_source["type"] = "htmlvue"
                new_source["key1"] = "$t"
                new_source["key3"] = False

                new_source["key2"] = MarkedList(
                    new_source["key2"]
                )
                new_source["toBeMarkedList"] = MarkedList(
                    new_source["toBeMarkedList"]
                )

                config["profiles"][pi]["key_source"][si] = new_source
                config["profiles"][pi]["key_source"] = config["profiles"][pi][
                    "key_source"]
                break

    return config


def main():
    configs = get_all_configs()

    for filename in configs:
        out_path = filename
        print(out_path)
        f = load_json(filename)
        new_config = replace_source(f, "source_key")
        new_config = parse_json(new_config)
        dump_json(out_path, new_config)


if __name__ == "__main__":
    main()
