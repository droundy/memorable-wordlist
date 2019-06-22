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

good_words = set(accuracy.keys())
for w in sorted(good_words):
    if accuracy[w] < 0.5:
        good_words.remove(w)
for w in sorted(good_words):
    if 'é' in w:
        good_words.remove(w)
print(sorted(good_words))
