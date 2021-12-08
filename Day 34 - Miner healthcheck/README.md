---
Author: Gvido Bērziņš
Date: 08.12.2021
---

Miner healthchecker for moneroocean and eth2miner.

## Usage

Run the script with Python

```
python readme_templater.py
```

The script will run in an infinite loop when launched.

## Purpose

This was used to check if my miner has gone offline, I had these problems
previously so I wrote a script to notify me of this case.

## How it works

The script simply queries the mining pool websites for status and based
on that sends a notification or not.
