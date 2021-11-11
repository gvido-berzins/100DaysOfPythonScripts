---
Author: Gvido Bērziņš
Date: 11.11.2021
---

Simple localization directory maker.

## Prerequisites

No need to install additional libraries, only standard library was used.

## Usage

Run the script with the `-h` flag to get help

```
$ python readme_templater.py -h
usage: lokalizer.py [-h] {php,js,ts,json,po,pot,mo,xliff,yaml} {single,namespace} ...
lokalizer.py: error: the following arguments are required: ext, sink_type
```

The `single` argument will create a directory with only locale files, but
`namespace` is meant to create multiple language files what are meant
as namespaces.

## Additionally

It is possible to create a binary with the `build.sh` script which requires
`pyinstaller`

```
pip install pyinstaller
```

The script is not needed, it runs `pyinstaller` and copies the binary to `~/.local/bin/`,
you can just do

```
pyinstall --onefile `lokalizer.py`
```

## Purpose

It depends on the user, because, this can really be a one time thing, It's
very simple, you run the script and it creates a directory for localization,
this was mostly a practice script for testing.
