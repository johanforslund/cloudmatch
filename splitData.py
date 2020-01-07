import pandas as pd
import json
import re

def clean_genre(s):
    #TODO: also remove "and" and switch "raphiphop" to "hiphoprap"
    regex = re.compile('[^a-zA-Z]')
    s = regex.sub('', s)
    return s.lower()

X = pd.read_json('./data/pop.json')
genres = pd.read_json('./data/genres.json')['genres']
users = X["favorite_tracks"]

genres = genres.values.tolist()

numOfGenres = len(genres)
midGenre = []

for user in users:
    meanGenre = [0] * numOfGenres
    for track in user:
        if not track['genre']:
            continue
        genre = clean_genre(track['genre'])
        try:
            idx = genres.index(genre)
        except ValueError:
            continue
        meanGenre[idx] += 1

    normalizer = sum(meanGenre)
    for i in range(0,len(meanGenre)):
        meanGenre[i] = meanGenre[i] / normalizer
    midGenre.append(meanGenre)

with open('./data/popSplit.json', 'w', encoding='utf8') as json_file:
    json.dump(midGenre, json_file, ensure_ascii=False)

