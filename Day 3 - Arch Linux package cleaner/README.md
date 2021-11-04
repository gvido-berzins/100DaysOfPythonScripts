---
Author: Gvido Bērziņš
Date: 04.11.2021
---

Learning `tkinter` was fun, but not initially intended, which led me to
not having a full nights sleep and not completing the script fully.

Planning to come back to this script, because I want to complete it
and a lot of time was wasted in fiddling with `tkinter`.

## Usage

There is no need for pip install, both scripts use standard library.

Just run the `tki.py` and you're set.

```
sudo python tki.py
```

## How it works

The main `tki.py` launches a GUI which is built with `tkinter`, from there
all packages are listed by using the `cleaner.py` script and then it
is possible to select the needed packages and remove the selected ones.

## To Do

- Choice to list or clean the packages only
- Make the `tkinter` GUI stable enough to rerun it without quitting
- List the packages in the GUI by date create/modified
- List packages/application from different scopes
- Create different removal methods instead of only `pacman`

