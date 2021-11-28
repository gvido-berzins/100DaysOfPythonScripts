---
Author: Gvido Bērziņš
Date: 28.11.2021
---

A simple fuzzer that I used for practicing XSS in https://portswigger.net/web-security/cross-site-scripting

## Prerequisites

Only `httpx` is required.

```
pip install -r requirements.txt
```

## Usage

```
python splurt.py http://example.com/?user=SPLURT tag
```

## Motivation

I know there are a lot of other fuzzers and I have used them, but this
was a quick idea I wanted to try out and leave this so that others may
be aware that it's not black magic, it's pretty easy build a basic one and
even a better one. :)
