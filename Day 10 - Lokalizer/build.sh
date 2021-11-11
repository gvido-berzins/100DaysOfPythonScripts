#!/bin/bash

pyinstaller --onefile lokalizer.py
cp dist/lokalizer ~/.local/bin/ -v
