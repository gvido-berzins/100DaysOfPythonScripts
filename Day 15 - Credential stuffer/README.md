---
Author: Gvido Bērziņš
Date: 17.11.2021
---

Work in progress credential sprayer, I wanted to make my own tool and decided to go with a script that tries the same credentials on all available services.

## Prerequisites

Impacket and other dependencies

```
pipenv install
```

## Usage

Run the script with Python with `-h` flag

```
% python creddy.py -h
usage: creddy.py [-h] [-s PORT] [-u USER] [-p PASSWORD] ip

positional arguments:
  ip                    IP to stuff

optional arguments:
  -h, --help            show this help message and exit
  -s PORT, --port PORT  Port to stuff, default is all
  -u USER, --user USER  Username to use
  -p PASSWORD, --pass PASSWORD
                        Password to use
```

## Purpose & Future

This little script is helping me understand more about socket programming
and networking.

I'm planning on continuously working on this script.
