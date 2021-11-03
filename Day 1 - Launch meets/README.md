---
author: Gvido Bērziņš
date: 02.11.2021
---

A simple script for launching the latest meeting in the browser by using Google Calendar API.

## Prerequisites

- OAuth2 credentials from Google Cloud Platform. ([more about that here](https://developers.google.com/workspace/guides/create-credentials))
- Python libraries `pip install -r requirements.txt`

## Usage

Just launch it with python, **but remember**, you need the `credentials.json` in the same directory as the script. (Or just modify the script constants)

```
python calmeet.py
```

To make it more usable add an alias for it.

```bash
alias meet="python ~/path/to/script/calmeet.py"
```

- or maybe a keybind to it, the rest is up to you.

## Links

- [Quickstart for Google Calendar API](https://developers.google.com/calendar/api/quickstart/python#step_1_install_the_google_client_library)
- [Creating credentials for the API](https://developers.google.com/workspace/guides/create-credentials)
