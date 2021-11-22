import neopixel
import machine
import time
import random

p = 5
n = 8
t = 1
d = 1
RED = 0
np = neopixel.NeoPixel(machine.Pin(p), n)
swf = True
swb = True

R, G, B = 190, 0, 196
r, g, b = 0, 0, 0

while True:
    RED += t

    if RED > 254:
        t = -1
    elif RED < 1:
        t = 1

    np[0] = (RED, 0, 0)
    np[1] = (RED, 0, 0)

    for i in range(2, n):
        np[i] = (r, g, b)

    if swf:
        d = 1
        swf = False
    elif swb:
        d = -1
        swb = False

    if (r == 0 and g == 0 and b == 0):
        swf = True
    elif (r == R and g == G and b == B):
        swb = True

    if r < R and d > 0:
        r += d
    elif r > 0 and d < 0:
        r -= 1

    if g < G and d > 0:
        g += d
    elif g > 0 and d < 0:
        g -= 1

    if b < B and d > 0:
        b += d
    elif b > 0 and d < 0:
        b -= 1

    np.write()
