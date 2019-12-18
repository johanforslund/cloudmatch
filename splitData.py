import pandas as pd
import json

X = pd.read_json('./data/pop.json')
users = X["favorite_tracks"]

rockCount = 0
popCount = 0
rapCount = 0

midGenre = []


for user in users:
    for track in user:
        if track['genre'] == 'Rock':
            rockCount += 1
        if track['genre'] == 'Pop':
            popCount += 1
        if track['genre'] == 'Hip-hop & Rap':
            rapCount += 1


    normalizer = (rockCount + popCount + rapCount)
    currentGenre = [rockCount/normalizer, popCount/normalizer, rapCount/normalizer]
    midGenre.append(currentGenre)
    rockCount = 0
    popCount = 0
    rapCount = 0

with open('popvsrockvsrap.json', 'w', encoding='utf8') as json_file:
    json.dump(midGenre, json_file, ensure_ascii=False)

