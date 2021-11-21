---
Author: Gvido Bērziņš
Date: 22.11.2021
---

One-line maker.

## Prerequisites

Only `pyperclip` for clipboard copy support.

## Usage

```
$ python3 powerpay.py -h
usage: powerpay.py [-h] [-f FILE] [-p PREFIX] [-n] [-d] [-m] [-c]

optional arguments:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  Filename for the powershell script, defaults to script.ps1
  -p PREFIX, --prefix PREFIX
                        Prefix for the script, defaults to
  -n, --noprefix        Don't use prefix
  -d, --noencode        Don't encode in base64
  -m, --noline          Prevent one-liner
  -c, --nocopy          Don't copy to clipboard
```

## Purpose

I created this script while practicing Active Directory enumerating and I
didn't want to write the powershell scripts in a remote machine.

This script is used to make one-liners which can be used in a shell, either
base64 encoded, plain, or even multi-line.

## To Do

Script is not finished and I want improvements to it for my use.

+ Add comment removal support for inline comments
