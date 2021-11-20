---
Author: Gvido Bērziņš
Date: 20.11.2021
---

Quick redis database for storing SIM card info

## Prerequisites

Redis installed in the system AND the python requirements in the requirements.txt

```
pip install -r requirements.txt
```

## Usage

Run the script with Python and `-h` flag to get the usage

```
$ python parsim.py
usage: parsim.py [-h] {g,ga,sa,gn,c,flushdb} [key ...]
parsim.py: error: the following arguments are required: command, key
```

## Note + How it works

I didn't have time for a new script so I wanted to post a script I
wrote beforehand.

There are not much useful docstrings and typing, so will quickly go over
the script.

The script has a few options for querying the data from the database

`g` - get a single record \
`ga` - get all \
`gn` - get all numbers \
`sa` - insert all \
`flushdb` - empty out the database

I left examples in the `input` directory, which is where the data for `sa`
mode is stored in, all of the data in there will be imported into the
database, where all of it is in the YAML format.

## Additional `app.py` Flask API

Additionally I wanted to access the database remotely, so I made a Flask
endpoint to get all of the data stored in the database through the API
I made.

This script can be also reproduced in any way desirable, I only added one
command, feel free to use the same script and add more to your use-case.
