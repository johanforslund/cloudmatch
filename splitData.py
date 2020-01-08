import pandas as pd
import json
import re

def clean_genre(s):
    #TODO: also remove "and" and switch "raphiphop" to "hiphoprap"
    regex = re.compile('[^a-zA-Z]')
    s = regex.sub('', s)
    return s.lower()

X = pd.read_json('./data/jazz.json')
genres = pd.read_json('./data/genres.json')['genres']

genres = genres.values.tolist()

numOfGenres = len(genres)
midGenre = []

for user_id, favorite_tracks in X.itertuples(index=False):
    meanGenre = [0] * numOfGenres
    for track in favorite_tracks:
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

    result = {user_id: meanGenre}
    
    midGenre.append(result)

with open('./data/jazzSplit.json', 'w', encoding='utf8') as json_file:
    json.dump(midGenre, json_file, ensure_ascii=False)

