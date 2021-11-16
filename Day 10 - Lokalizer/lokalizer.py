import argparse
import os
from dataclasses import dataclass, field
from enum import Enum

# Defaults
DEFAULT_NAMESPACES = ["messages", "validators", "forms"]
DEFAULT_DIRS = ["locale", "translations", "lang", "language", "i18n"]
DEFAULT_LOCALE = "en"
DEFAULT_LOCALES = ["en", "ru", "de"]
EXT_CHOICES = ["php", "js", "ts", "json", "po", "pot", "mo", "xliff", "yaml"]
YAML_TEMPLATE = ""
JSON_TEMPLATE = "{}"
JS_TEMPLATE = "export defaults {}"
TS_TEMPLATE = "export defaults {}"
PHP_TEMPLATE = "<?php\n\nreturn [];"
POT_TEMPLATE = '''
msgid ""
msgstr ""
"Project-Id-Version: \\n"
"POT-Creation-Date: 2021-06-17 10:18+0300\\n"
"PO-Revision-Date: 2021-06-17 10:19+0300\\n"
"Last-Translator: \\n"
"Language-Team: \\n"
"MIME-Version: 1.0\\n"
"Content-Type: text/plain; charset=UTF-8\\n"
"Content-Transfer-Encoding: 8bit\\n"
"X-Generator: Poedit 2.4.2\\n"
"X-Poedit-Basepath: .\\n"
"Plural-Forms: nplurals=2; plural=(n != 1);\\n"
"Language: en\\n"
'''
PO_TEMPLATE = POT_TEMPLATE
MO_TEMPLATE = POT_TEMPLATE
XLIFF_TEMPLATE = """<?xml version="1.0"?>
<xliff version="1.2" xmlns="urn:oasis:names:tc:xliff:document:1.2">
    <file source-language="en" target-language="en" datatype="plaintext" original="file.ext">
        <body>
        </body>
    </file>
</xliff>
"""


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments"""
    # Argument choices
    SINGLE_DIR_CHOICES = ["root", "dir", "nested"]
    NAMESPACED_DIR_CHOICES = ["root", "dir", "lang_dir"]

    parser = argparse.ArgumentParser()
    parser.add_argument("ext", choices=EXT_CHOICES)
    subparser = parser.add_subparsers(title="Sink Type", dest="sink_type")
    subparser.required = True

    single_group = subparser.add_parser("single")
    namespace_group = subparser.add_parser("namespace")

    single_group.add_argument("-s",
                              "--structure",
                              choices=SINGLE_DIR_CHOICES,
                              default="root")

    namespace_group.add_argument("-s",
                                 "--structure",
                                 choices=NAMESPACED_DIR_CHOICES,
                                 default="dir")
    return parser.parse_args()


@dataclass
class Sink:
    """Class representing a single sink structure"""


@dataclass
class SingleSink(Sink):
    """Class representing a single sink structure"""


@dataclass
class NamespacedSink(Sink):
    """Class representing a namespaced sink structure"""


class SinkTypes(Enum):
    """Class representing a sink type"""

    SINGLE = "single"
    NAMESPACED = "namespaced"


class StructureTypes(Enum):
    """Class representing a sink type"""

    ROOT = "root"
    DIR = "dir"
    NESTED = "nested"  # nth nested
    LANG_DIR = "lang_dir"  # lang dirs inside a dir


@dataclass
class DirStructure:
    """Class representing a directory structure"""

    type_: StructureTypes
    structure: list = field(default_factory=list)
    dir_name: str = field(default=DEFAULT_DIRS[0])

    def __post_init__(self):
        if self.type_ == StructureTypes.ROOT:
            pass

        if self.type_ == StructureTypes.DIR:
            self.structure.append(self.dir_name)

        if self.type_ == StructureTypes.LANG_DIR:
            for locale in DEFAULT_LOCALES:
                self.structure.append(os.path.join(self.dir_name, locale))


def get_sink(type_) -> Sink:
    if type_ == SinkTypes.SINGLE.value:
        return SingleSink()

    elif type_ == SinkTypes.NAMESPACED.value:
        return NamespacedSink()


def get_dir_structure(type_) -> DirStructure:
    """Return a directory structure"""
    if type_ == StructureTypes.ROOT.value:
        return DirStructure(StructureTypes.ROOT)

    if type_ == StructureTypes.DIR.value:
        return DirStructure(StructureTypes.DIR)

    if type_ == StructureTypes.LANG_DIR.value:
        return DirStructure(StructureTypes.LANG_DIR)


@dataclass
class StructureMaker:
    """Class representing the structure maker"""
    @staticmethod
    def create_structure(ext: str, sink: Sink,
                         structure: DirStructure) -> None:
        """Create a lokalization directory structure"""
        filenames = ([DEFAULT_LOCALE]
                     if isinstance(sink, SingleSink) else DEFAULT_NAMESPACES)
        filenames = prepare_files(filenames, ext)

        if structure.type_ == StructureTypes.ROOT:
            create_files(filenames, ext)

        elif structure.type_ == StructureTypes.DIR:
            for directory in structure.structure:
                os.makedirs(directory, exist_ok=True)
                create_files([
                    os.path.join(directory, filename) for filename in filenames
                ], ext)

        elif structure.type_ == StructureTypes.LANG_DIR:
            for directory in structure.structure:
                os.makedirs(directory, exist_ok=True)
                create_files([
                    os.path.join(directory, filename) for filename in filenames
                ], ext)


def prepare_files(filenames: list[str], ext: str) -> list[str]:
    """Prepare a list of files"""
    return [f"{f}.{ext}" for f in filenames]


def create_files(filenames: list[str], ext: str) -> None:
    """Create language files"""
    for filename in filenames:
        path = os.path.join(cwd, filename)
        create_file_by_ext_template(path, ext)
        # create_empty_file(path)


def create_empty_file(filename: str) -> None:
    open(filename, "w").close()


def create_file_by_ext_template(filename: str, ext: str) -> None:
    """Create a file with the specific contents of the file extension"""
    template_name = f"{ext}_template".upper()
    contents = globals()[template_name]
    with open(filename, "w") as f:
        f.write(contents)


def main():
    global cwd
    cwd = os.getcwd()
    ext = args.ext
    sink: Sink = get_sink(args.sink_type)
    structure: DirStructure = get_dir_structure(args.structure)
    structure_maker = StructureMaker()
    structure_maker.create_structure(ext, sink, structure)


if __name__ == "__main__":
    args = parse_args()
    print(args)
    main()
