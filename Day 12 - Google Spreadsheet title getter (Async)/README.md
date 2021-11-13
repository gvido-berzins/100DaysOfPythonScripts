---
Author: Gvido Bērziņš
Date: 13.11.2021
---

A simple Google Spreadsheet title getter, asynchronously get spreadsheet titles or perform other operations with small adjustments.

## Prerequisites

Google Sheets API service account credentials in the current working directory or different one (just change the path in code)

```
pip install -r requirements.txt
```

## Usage

Run the script with Python

```
python get_titles.py
```

## Why?

I had a small task to get the titles from spreadsheets and that's it, but this script can be repurposed to do more operations, you
just need to modify `get_spreadsheet_title_async` function or just change it to something similar.
