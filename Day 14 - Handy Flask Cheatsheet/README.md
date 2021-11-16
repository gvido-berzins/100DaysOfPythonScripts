---
Author: Gvido Bērziņš
Date: 16.11.2021
---

Simple Question & Answer lookup cheatsheet using a Flask front-end.

## Prerequisites

Flask and aiken formatted data without empty lines and only 4 multiple choice questions.

```
pip install -r requirements.txt
```

## Usage

Run the following command to start a Flask app and it will be available.

```
export FLASK_APP=solver-app.py; flask run
```

## Purpose

I had a test to complete and in my previous studies, there were the exact
same questions and answers, so I decided to reuse the data and create
a cheatsheet, flask part was, so that I can easily lookup the answers
from the Flask webapp.

As you can see the app has very specific constraints and the code quality
is lower than usual, this is because of it being a quick hack-together.
