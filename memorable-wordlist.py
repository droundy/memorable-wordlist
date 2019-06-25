import numpy as np
import urllib.request
import requests
import io
import zipfile
import pandas as pd

def download_extract_zip(url, fname):
    """
    Download a ZIP file and extract its contents in memory
    yields (filename, file-like object) pairs
    """
    response = requests.get(url)
    with zipfile.ZipFile(io.BytesIO(response.content)) as thezip:
        return thezip.open(fname)

opener = urllib.request.FancyURLopener({})

accuracy = {}
response_time = {}

badwords = set()
with opener.open('https://www.cs.cmu.edu/~biglou/resources/bad-words.txt') as f:
    for l in f.readlines():
        badwords.add(l.decode('utf-8').replace('\n',''))
with download_extract_zip("http://crr.ugent.be/blp/txt/blp-items.txt.zip",
                          "blp-items.txt") as f:
    for l in f.readlines():
        fields = l.decode('utf-8').split('\t')
        if fields[1] == 'W' and fields[2] != 'NA':
            # it is an actual word
            word = fields[0]
            accuracy[word] = float(fields[4])
            response_time[word] = float(fields[2])

aoa_test_based = {}
aoa_rating = {}
aoa = {}
aoa_file = pd.read_excel('http://crr.ugent.be/papers/Master%20file%20with%20all%20values%20for%20test%20based%20AoA%20measures.xlsx')
for i in range(aoa_file.shape[0]):
    w = aoa_file.get_value(col='WORD', index=i)
    a = []
    if aoa_file.get_value(col='AoAtestbased', index=i) != '#N/A':
        aoa_test_based[w] = float(aoa_file.get_value(col='AoAtestbased', index=i))
        a.append(aoa_test_based[w])
    if aoa_file.get_value(col='AoArating', index=i) != '#N/A':
        aoa_rating[w] = float(aoa_file.get_value(col='AoArating', index=i))
        if aoa_rating[w] != aoa_rating[w]:
            del aoa_rating[w]
        else:
            a.append(aoa_rating[w])
    if len(a) > 0:
        aoa[w] = sum(a)/len(a)

gsl_freq = {}
gsl_file = pd.read_excel('http://www.newgeneralservicelist.org/s/NGSL-101-with-SFI.xlsx')
for i in range(gsl_file.shape[0]):
    w = gsl_file.get_value(col='Lemma', index=i)
    gsl_freq[w] = gsl_file.get_value(col='Coverage', index=i)
gsl_freq_norm = gsl_freq['dog'] # normalize to dog
for w in gsl_freq.keys():
    gsl_freq[w] /= gsl_freq_norm

subtitles_freq = {}
with opener.open("https://raw.githubusercontent.com/hermitdave/FrequencyWords/master/content/2018/en/en_full.txt") as f:
    for l in f.readlines():
        fields = l.decode('utf-8').split(' ')
        subtitles_freq[fields[0]] = float(fields[1])/125769 # normalize to dog
subtitles_freq_norm = subtitles_freq['dog'] # normalize to dog
for w in subtitles_freq.keys():
    subtitles_freq[w] /= subtitles_freq_norm
min_freq = min(subtitles_freq.values())

def get_freq(w):
    if w in gsl_freq:
        return gsl_freq[w]
    elif w in subtitles_freq:
        return subtitles_freq[w]
    return min_freq

concreteness = {}
percent_known = {}
with opener.open('http://crr.ugent.be/papers/Concreteness_ratings_Brysbaert_et_al_BRM.txt') as f:
    for l in f.readlines():
        fields = l.decode('utf-8').split('\t')
        if fields[1] == 'Bigram':
            continue # this is the first line
        if fields[1] == '1':
            continue # this is a bigram, and let us just skip them
        concreteness[fields[0]] = float(fields[2])
        percent_known[fields[0]] = float(fields[6])

# In each case higher is more memorable, but in the case of valence
# small numbers may mean things to absolutely avoid.
valence = {}
arousal = {}
dominance = {}
with opener.open('http://crr.ugent.be/papers/Ratings_Warriner_et_al.csv') as f:
    for l in f.readlines():
        fields = l.decode('utf-8').split(',')
        if fields[2] == 'V.Mean.Sum':
            continue # this is the first line
        valence[fields[1]] = float(fields[2])
        arousal[fields[1]] = float(fields[5])
        dominance[fields[1]] = float(fields[8])

min_valence = 4
def get_valence(w):
    if w in valence:
        return valence[w]
    values = []
    for x in valence.keys():
        if w in x:
            values.append(valence[x])
    for x in valence.keys():
        if x in w:
             values.append(valence[x])
    v = sum(values+[min_valence])/(len(values)+1)
    if v < min_valence:
        return v
    return min_valence

good_words = set(percent_known.keys())
for w in sorted(good_words):
    if 'é' in w:
        good_words.remove(w)
    elif w in badwords:
        good_words.remove(w)

def rescale_rating(x, xok):
    return np.log10(x/xok)
def rescale_linear(x, xok, scale=1):
    return (x-xok)/scale
def rescale_rating_with_penalty(x, xok, scale=0):
    if x > xok:
        return np.log10(x/xok)
    elif scale == 0:
        return 10*(x - xok)/xok
    else:
        return 10*(x - xok)/scale
def rescale_linear_with_penalty(x, xok, scale=1):
    if x > xok:
        return (x-xok)/scale
    else:
        return 1-np.exp((xok-x)/scale)

def rating(word, verbose=False):
    value = 0.
    if word in aoa:
        v = -rescale_linear(aoa[word], 15, scale=5)
        if verbose:
            print('                               aoa %.2g' % aoa[word], '-> %.2g' % v)
        value += v
    if word in concreteness:
        v = rescale_linear(concreteness[word], 2, scale=0.5)
        if verbose:
            print('                      concreteness', concreteness[word], '-> %.2g' % v)
        value += v
    if word in accuracy:
        v = rescale_linear_with_penalty(accuracy[word], 0.7)
        if verbose:
            print('                          accuracy %.2g' % accuracy[word], '-> %.2g' % v)
        value += v
    if word in percent_known:
        v = rescale_linear_with_penalty(percent_known[word],0.8)
        if verbose:
            print('                     percent_known', percent_known[word], '-> %.2g' % v)
        value += v
    if word in arousal:
        v = rescale_linear(arousal[word],2,scale=5)
        if verbose:
            print('                           arousal', arousal[word], '-> %.2g' % v)
        value += v
    if word in dominance:
        v = rescale_linear(dominance[word],2,scale=5)
        if verbose:
            print('                          dominance', dominance[word], '-> %.2g' % v)
        value += v

    v = get_valence(word)
    val_value = rescale_linear_with_penalty(v, min_valence,scale=3)
    if verbose:
        if word in valence:
            print('                           valence', v, '-> %.2g' % val_value)
        else:
            print('                          *valence', v, '-> %.2g' % val_value)
    value += val_value

    f = get_freq(word)
    v = rescale_rating(f, 1)
    value += v
    if verbose:
        print('                              freq %.3g -> %.3g' % (f, v))

    value -= len(word)/10

    return value

ordered = list(reversed(sorted(good_words, key=lambda w: rating(w))))


with open('src/words.rs', 'w') as f:
    f.write('pub const LIST: &[&str] = &[\n')
    which = 0
    for w in ordered[:1<<14]:
        f.write('   "%s",\n' % w)
        r = rating(w)
        print('%5d: %15s %.4g' % (which, w, r))
        rating(w, True)
        which += 1
    f.write('];\n')
