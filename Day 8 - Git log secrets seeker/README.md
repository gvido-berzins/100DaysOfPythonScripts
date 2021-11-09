---
Author: Gvido Bērziņš
Date: 09.11.2021
---

A simple script to search for keywords in a git repository.

## Prerequisites

The only things that are required are, access to the git repository you are cloning and the GitPython library.

```
pip install -r requirements.txt
```

## Usage

There are a few filters I have created, to list all the arguments.

For the repository argument I was using my personal PoC repository, which
you can use also.

- https://github.com/gvido-berzins/git-log-secrets-poc

```
$ python secret_seeker.py -h
usage: secret_seeker.py [-h] [-c] [-s] [-u] [-l] [-k KEYWORDS] repository

Git commit secret finder

positional arguments:
  repository            URL or the path to the git repository

optional arguments:
  -h, --help            show this help message and exit
  -c, --clone           Clone a repository
  -s, --sensitive       Case sensitive search
  -u, --upper           Search for the keywords in uppercase
  -l, --lower           Search for the keywords in lowercase
  -k KEYWORDS, --keywords KEYWORDS
                        Comma separated list of keywords to search for
```

## Purpose

The purpose of this script is to remind the git user that git knows
everything, this is good, but can lead to some nasty outcomes.

**REMEMBER**, be carefull what you commit and push, because every change
is logged and if there was an ACTIVELY used API key or secret, anyone,
would be able to find it with a simple `git grep`.

Another use for this script is for people to check if their repositories,
contain such things, this might occure when open sourcing the repository or
just validating just in case.

## Mitigations

The easiest way would be to start a clean repository and copy all the code
to that one, this way only the added code would show up the changes, just
don't copy over the `git/` repository!

I'm not sure about how it goes about removing commits from the log selectively,
I found [this](https://stackoverflow.com/questions/495345/how-to-remove-selected-commit-log-entries-from-a-git-repository-while-keeping-th/495352) about how to remove them locally, but
not quite sure about removing globally from the whole history.
