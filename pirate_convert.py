from arrr import translate
from datetime import datetime

english = "Hello there. How are you?"
english = "pirate hello there. how are you today?"
english ="That's because it's such a nice one."
pirate = translate(english)
print(pirate)


# Load Movielines & Conversations
movie_lines = {}
movie_lines_pirate = {}

for line in open("./cornell movie-dialogs corpus/movie_lines.txt",
                 encoding="latin1"):
    line = line.strip()
    parts = line.split(" +++$+++ ")
    if len(parts) == 5:
        movie_lines_pirate[parts[0]] = translate(parts[4])
        movie_lines[parts[0]] = parts[4]
    else:
        movie_lines[parts[0]] = ""
        movie_lines_pirate[parts[0]] = ""

import csv
with open('pirate_convert.csv', 'w') as f:
    for key in movie_lines_pirate.keys():
        f.write("%s, %s\n" % (key, dict[key]))


# Force updates
# Load Movielines & Conversations
movie_lines = {}
movie_lines_pirate = {}

count = 1
for line in open("./cornell movie-dialogs corpus/movie_lines.txt",
                 encoding="latin1"):
    line = line.strip()
    parts = line.split(" +++$+++ ")
    translated = False
    wait = 3.0
    startTime = datetime.now()
    if len(parts) == 5:
        while not translated:
            pirate_translation = translate(parts[4])
            search_time = datetime.now()
            if pirate_translation != parts[4] or (search_time - startTime).total_seconds() > wait:
                movie_lines_pirate[parts[0]] = pirate_translation
                movie_lines[parts[0]] = parts[4]
                translated = True
                count += 1
                print(pirate_translation, parts[0], count)
    else:
        movie_lines[parts[0]] = ""
        movie_lines_pirate[parts[0]] = ""

import pandas as pd
(pd.DataFrame.from_dict(data=movie_lines_pirate, orient='index')
   .to_csv('pirate_convert.csv', header=False))