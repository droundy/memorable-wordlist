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

# In each case higher is more memorable, but in the case of valence
# small numbers may mean things to absolutely avoid.
valence = {}
arousal = {}
dominance = {}
with open('affective_ratings.txt') as f:
    for l in f.readlines():
        fields = l.split(',')
        if fields[2] == 'V.Mean.Sum':
            continue # this is the first line
        valence[fields[1]] = float(fields[2])
        arousal[fields[1]] = float(fields[5])
        dominance[fields[1]] = float(fields[8])

good_words = set(accuracy.keys())
for w in sorted(good_words):
    if accuracy[w] < 0.6:
        good_words.remove(w)
for w in sorted(good_words):
    if 'é' in w:
        good_words.remove(w)
print(sorted(good_words))

def rating(word, verbose=False):
    value = 0.
    if word in concreteness:
        if verbose:
            print('                 concreteness', concreteness[word])
        value += concreteness[word]*10
    if word in valence:
        min_valence = 3
        if verbose:
            print('                      valence', valence[word])
        if valence[word] < min_valence:
            value += 100*(valence[word] - 3)
        else:
            value += 10*(valence[word] - 3)
    return value

for w in sorted(good_words) + ['dog', 'cat', 'kitten', 'pedophile', 'murder']:
    r = rating(w)
    print('%15s %.4g' % (w, r))
    rating(w, True)

print('total', len(good_words))
