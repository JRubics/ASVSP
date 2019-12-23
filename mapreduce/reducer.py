#!/usr/bin/python
import sys 

current_cloud_type = ""
current_count = 0
cloud_type = ""
count = 0

for line in sys.stdin: 
    line = line.strip()
    tokens = line.split(',')
    cloud_type = tokens[0]
    count = tokens[1]
    try:
        count = int(count)
    except ValueError:
        # Count was not a number, so silently ignore this line
        continue
    if current_cloud_type == cloud_type: 
        current_count += count 
    else: 
        if current_cloud_type:
            print ('%s\t%s' % (current_cloud_type, current_count))
        current_count = count
        current_cloud_type = cloud_type

if current_cloud_type == cloud_type: 
    print ('%s\t%s' % (current_cloud_type, current_count))