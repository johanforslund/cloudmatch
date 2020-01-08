from sklearn.neighbors import NearestNeighbors
import numpy as np
import pandas as pd
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


X = pd.read_json('./data/splitAll2.json')
print("Finished reading split")
Y = read_data()
print("Finished reading data")

X_test = [[0] * 126]
X_test[0][99] = 1.0

#X_test = np.random.dirichlet(np.ones(126), size=1)

#X_test = [ran.random() for i in range(1,127)]
#s = sum(X_test)
#X_test = [i/s for i in X_test]
#X_test = [X_test]

k = 16
knn = NearestNeighbors(n_neighbors=k)

knn.fit(X)
pred = knn.kneighbors(X_test)
#print(X_test)
print(X.iloc[pred[1][0][0]])
print("Pred")
print(pred)
#TODO: add dictionary with track_ids and their number of occurrences
#Weight algorithm for recommending tracks
rec_tracks = {}

for i in range(0,k):
    #dist = pred[0][0][i]
    for track in Y["favorite_tracks"][pred[1][0][i]]:
        #TODO: calculate score here
        #TODO: filter podcast and live
        if track['genre'] and clean_genre(track['genre']) != 'rock': 
            continue
        if track['likes_count'] > 5000:
            continue
        if track['id'] in rec_tracks:
            rec_tracks[track['id']] += 1
        else:
            rec_tracks[track['id']] = 1

maxScore = {'id': 0, 'score': 0}

for track in rec_tracks:
    if rec_tracks[track] > maxScore['score'] and rec_tracks[track] < k: # Improve this
        maxScore['score'] = rec_tracks[track]
        maxScore['id'] = track

for i in range(0,k):
    for track in Y["favorite_tracks"][pred[1][0][i]]:
        if track['id'] == maxScore['id']:
            print(track['permalink_url'])
            print(maxScore['score'])
            print(track['id'])
            pass

#print(maxScore)
