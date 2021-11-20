---
Author: Gvido Bērziņš
Date: 20.11.2021
---

Simple package searcher.

## Prerequisites

```
pip install -r requirements.txt
```


## Usage

```
$ python lookup_package.py
usage: lookup_package.py [-h] [-d DATABASES] package_name

$ python lookup_package.py -d aurpackagedatabase python
$ python lookup_package.py -d aurpackagedatabase,archpackagedatabase python
$ python lookup_package.py python # To search all
```


## Extending it

The script can be easily extended, to do it repeat the Database by the
`PackageDabase` structure and put it in the `ALL_DATABASES` list and that's
it.

## To Do

PyPi package index is really slow, because the `simple/` endpoint retreives
every existing package. The page loads already a while in my browser.

- TODO: Make it async
  - The JSON request spider part
