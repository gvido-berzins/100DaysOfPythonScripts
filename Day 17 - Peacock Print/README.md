---
Author: Gvido Bērziņš
Date: 18.11.2021
---

Pretty printer using `colorama`

## Prerequisites

The only requirement is `colorama`

```
pip install -r requirements.txt
pipenv install
```

## Usage

I wrote a demo, which is available in the script, here's the snippet.

```python
# Calling it straight away
pp = PeacockPrint
print(pp("text~f hello", ("cyan",)))

# Defining it as a variable
good_template = "~fgreen~r ~s~bred tem~r~s~fplate"
good_pretty_text = PeacockPrint(
    good_template, ("green", "BRIGHT", "red", "DIM", "LIGHTBLUE")
)
print(good_pretty_text)
# good_pretty_text.text <-- to get the string

# Mismatching replacement count and color count
bad_template = "~fgreen ~fred tem~rplate"
bad_pretty_text = PeacockPrint(bad_template, ("green", "red", "blue"))
print(bad_pretty_text)
```

## Purpose

I got sick of making my own versions of pretty printers and had some limitations,
but I found colorama from awesome-python repository, it still wasn't enough
I wanted it to be easier to choose where to color.

There is probably something like this out the, but this was a good practice for
me.
