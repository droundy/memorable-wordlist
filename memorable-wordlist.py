import numpy as np

accuracy = {}
response_time = {}

with open('blp-items.txt') as f:
    for l in f.readlines():
        fields = l.split('\t')
        if fields[1] == 'W' and fields[2] != 'NA':
            # it is an actual word
            word = fields[0]
            accuracy[word] = float(fields[4])
            response_time[word] = float(fields[2])
        else:
            print(fields[1], fields)

print(accuracy)
