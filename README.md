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

### aoa.txt affective_ratings.txt blp-items.txt and concreteness.txt

These files each represent lexical research data compiled by
[The Center for Reading Research at Ghent](http://crr.ugent.be/).
This data includes word ratings of age of acquisition (`aoa.txt`),
concreteness (`concreteness.txt`), valence and arousal
(`affective_ratings`).  There is also a list of word prevalence
(i.e. what fraction of people know the words) in `blp-items.txt`.

### gsl.txt

### en_full.txt

A
[list of word frequencies](https://github.com/hermitdave/FrequencyWords)
compiled from the OpenSubtitles database.  This list is licensed with
a CC-by-sa-3.0 license by Hermit Dave.

### bad-words.txt

A list of "bad words" which might be considered offensive in randomly
generated output from
[Luis von Ahn's research croup](https://www.cs.cmu.edu/~biglou/resources/).
Note that some of these aren't actually bad words, but are words that
in combination might seem bad or irreverent.

## Example output with 44 bits entropy

`space_delimited`:
```
board curved deep want
choose pianist obey first
skinny public steer skate
catfish orchid peanuts sticky
camel footprint clock cook
get food trot olive
gift learner stair they
feel carry free doorman
meteorite baggage toothpaste pupil
```
`snake_case`:
```
welcome_table_lifeboat_trophy
speedy_meteorite_beach_wee
doorman_woman_fluffy_youngster
two_midnight_teapot_hope
dance_wheel_ballroom_kind
wealth_seaside_diner_question
friend_helmet_canyon_biscuit
kiss_wing_cherry_cartoon
name_free_name_suitcase
```
`kebab_case`:
```
icebox-core-elf-cure
spice-a-trust-cute
loop-doodle-carpet-silent
atlas-arrow-sandwich-cruise
sparrow-wheat-grapefruit-meatball
on-glee-paw-painting
live-strawberry-plaster-clock
smash-sparkle-jazz-wet
advance-sherbet-mix-tour
```
`camel_case`:
```
SnakePastaYoungMousetrap
FreezeKisserWetBuzzer
ModelPraiseRhythmPlace
TeaTraySwordfishJelly
FancyIcebergGingerReceipt
PantryYellowExpectBend
RelaxSneezeSpreadToothpaste
DrumSeatIcedPlant
HamGlassOxYear
```
