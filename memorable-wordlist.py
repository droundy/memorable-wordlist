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

aoa_test_based = {}
aoa_rating = {}
with open('aoa.txt') as f:
    for l in f.readlines():
        fields = l.split('\t')
        if fields[1] == 'MEANING':
            continue # this is the first line
        if fields[2] != '#N/A':
            aoa_test_based[fields[0]] = float(fields[2])
        if fields[3] != '#N/A' and len(fields[3]) > 0:
            aoa_rating[fields[0]] = float(fields[3])

concreteness = {}
percent_known = {}
with open('concreteness.txt') as f:
    for l in f.readlines():
        fields = l.split('\t')
        if fields[1] == 'Bigram':
            continue # this is the first line
        concreteness[fields[0]] = float(fields[2])
        percent_known[fields[0]] = float(fields[6])

good_words = set(accuracy.keys())
for w in sorted(good_words):
    if accuracy[w] < 0.6:
        good_words.remove(w)
for w in sorted(good_words):
    if 'é' in w:
        good_words.remove(w)
print(sorted(good_words))

print('total', len(good_words))
