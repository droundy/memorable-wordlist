# Memorable wordlist

This is a list of words that are intended to be memorable (and
unobjectionable) for use in
[correct horse battery staple](https://m.xkcd.com/936) style
passphrase generators.  The word list is generated based on a number
of sources using a simple python script, and is intended to be
something that will be improved upon.

The word list is provided as a rust crate, which also includes a few
simple passphrase generators using the standard
[cryptographically secure random number generator](https://rust-random.github.io/rand/rand/fn.thread_rng.html).
See the documentation for details.

## Process

The alogrithm to generate the list is in `memorable-wordlist.py`.
Basically, I came up with a hokey value for words based on wanting
words to be *short*, *familiar*, *not bad*, and ideally either
*concrete* (meaning something you can visualize) or *exciting*.  I
expect I can do better, and intend to do so over time.  Patches are
most welcome, as well as bug reports (e.g. if two words are
significantly out of order on a subjective basis).

Note that my set of sources is the same as that of the
[EFF wordlist](https://www.eff.org/deeplinks/2016/07/new-wordlists-random-passphrases)
but that list does not publish its algorithm, and the algorithm used is
obviously screwed up, since neither `dog` nor `cat` appear in the
lists.  What could be more concrete than those?

## Sources

The `memorable-wordlist.py` script downloads and uses a variety of
lexical data to decide which words will be most appropriate.  Several
of the sources come from lexical research data compiled by
[The Center for Reading Research at Ghent](http://crr.ugent.be/).
This data includes word ratings of age of acquisition, concreteness,
valence and arousal.  There is also a file full of word prevalence
data (i.e. what fraction of people know the words).

We further use the frequency tables from the
[New General Service List](http://www.newgeneralservicelist.org),
which is a set of words for English language learners to learn.  In
addition, we use a
[list of word frequencies](https://github.com/hermitdave/FrequencyWords)
compiled from the OpenSubtitles database.

Finally, we download a list of "bad words" which might be considered
offensive in randomly generated output from
[Luis von Ahn's research croup](https://www.cs.cmu.edu/~biglou/resources/).
Note that some of these aren't actually bad words, but are words that
in combination might seem bad or irreverent.

## Example output with 44 bits entropy

`space_delimited`:
```
snowman sleigh redwood cow
zebra launch peanuts nest
vine lung thigh glove
marshmallow airplane seal pear
smooch sofa guidebook thank
lawyer tornado field cradle
pilot mango waiter cream
iron ad villa trailer
bookshop temple coat fry
```
`snake_case`:
```
suitcase_yellow_coast_street
kids_rhino_bear_giraffe
kitchen_elm_certificate_handle
poodle_mower_ranch_street
mixture_pencil_bump_tall
embryo_aunt_dairy_swimsuit
reporter_festival_wax_nylon
buyer_hour_bowl_print
pit_cloth_lunch_hummingbird
```
`kebab_case`:
```
spoon-tractor-tree-farm
pepper-rocket-hillside-coin
clown-singer-parachute-wasp
snout-door-cradle-tuna
blink-museum-laugh-pin
meteor-first-girl-talk
bamboo-crate-chick-rifle
song-swim-fortress-bathroom
whip-mat-park-reindeer
```
`camel_case`:
```
JawParadeAuthorRocket
HeelTuxedoThunderstormLady
OceanItemStudyHospital
TeaspoonRubModelHorizon
NostrilWallpaperGroupPup
BangPodSaleLace
MeterLightingRobotWallet
InkHomeRiverStairway
GolfLaughTextbookHamster
```
