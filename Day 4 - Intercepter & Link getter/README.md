---
Author: Gvido Bērziņš
Date: 05.11.2021
---

Was stuck in a rabbit hole in making a TCP proxy from scratch.

I found out about `twisted` after wasting a lot of time, but I want to
get back to this, after I learn to use `twisted`.

The main idea of this script was to:
- Intercept all request headers
- Get all requested resources/links
- Parse all of the JS/CSS/HTML (etc.) content
- Get all links found in the parsed content
