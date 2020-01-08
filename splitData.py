import pandas as pd
import json
import re

def read_data():
    A = pd.read_json('./data/acoustic.json')
    B = pd.read_json('./data/bass.json')
    C = pd.read_json('./data/blues.json')
    D = pd.read_json('./data/classical.json')
    E = pd.read_json('./data/country.json')
    F = pd.read_json('./data/dubstep.json')
    G = pd.read_json('./data/edm.json')
    H = pd.read_json('./data/folk.json')
    I = pd.read_json('./data/hiphop.json')
    J = pd.read_json('./data/house.json')
    K = pd.read_json('./data/jazz.json')
    L = pd.read_json('./data/latin.json')
    M = pd.read_json('./data/metal.json')
    N = pd.read_json('./data/pop.json')
    O = pd.read_json('./data/rap.json')
    P = pd.read_json('./data/rnb.json')
    Q = pd.read_json('./data/rock.json')
    R = pd.read_json('./data/singersongwriter.json')
    S = pd.read_json('./data/soul.json')
    T = pd.read_json('./data/soundtrack.json')
    U = pd.read_json('./data/techno.json')
    V = pd.read_json('./data/trap.json')
    W = pd.read_json('./data/world.json')
    return pd.concat([A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T,U,V,W]).drop_duplicates(subset='user_id').reset_index(drop=True)

def clean_genre(s):
    #TODO: also remove "and" and switch "raphiphop" to "hiphoprap"
    regex = re.compile('[^a-zA-Z]')
    s = regex.sub('', s)
    return s.lower()

X = read_data()

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
    if normalizer == 0:
        normalizer = 1
    for i in range(0,len(meanGenre)):
        meanGenre[i] = meanGenre[i] / normalizer

    #result = {user_id: meanGenre} not used anymore?
    
    midGenre.append(meanGenre)

with open('./data/splitAll2.json', 'w', encoding='utf8') as json_file:
    json.dump(midGenre, json_file, ensure_ascii=False)

