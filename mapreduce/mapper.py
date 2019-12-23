#!/usr/bin/python
import sys
import math

# izracunaj ghi, izbaci gde je 0
for line in sys.stdin:
    line = line.strip()
    words = line.split("\t")
    timestamp = words[0]
    timestamp = timestamp.split(" ")
    date = timestamp[0]
    time = timestamp[1]
    temperature = words[6]
    dhi = int(words[7])
    dni = int(words[8])
    angle = float(words[9])
    ghi = dhi + (dni * (math.cos(angle * math.pi / 180)))
    print ('%s, %lf, %s' % (date, ghi, line))
