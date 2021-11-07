---
Author: Gvido Bērziņš
Date: 06.11.2021
---

This script is meant to be used for Linux Local privilege escalation and
enumeration.

I didn't implement all the features I wanted (like automatic detection
for misconfiguration), but I'm satisfied for, now, because it runs almost
all the commands I would run manually.

## Prerequisites

If you want a single file solution, the just `pip install pyinstaller`
and create a binary with

```
pyinstaller misconf.py --onefile
```

The rest of the used libraries are from standard library.

## Usage

Just run it.

```
python misconf.py
```

## Inspiration

The main inspiration comes from the [PEAS-ng](https://github.com/carlospolop/PEASS-ng/tree/master/linPEAS) project, combined with [g-tmi1l's](https://blog.g0tmi1k.com/2011/08/basic-linux-privilege-escalation/) blog.

## Next steps

I would like to make this script into a single line, because sometimes, it
is bothersome to get the file on the system and then execute it.

Adding alerts for misconfiguration (the main idea of this), like throwing
an alert for writable `/etc/passwd`.
