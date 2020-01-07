from sklearn.neighbors import NearestNeighbors
import numpy as np
import pandas as pd

X = pd.read_json('./data/popSplit.json')
Y = pd.read_json('./data/pop.json')

X_test = [[0] * 126]
X_test[0][52] = 1.0
#X_test = np.random.dirichlet(np.ones(126), size=1)

k = 7
knn = NearestNeighbors(n_neighbors=k)
knn.fit(X)
pred = knn.kneighbors(X_test)
#print(X_test)
#print(X.iloc[pred[1][0][0]])
#TODO: add dictionary with track_ids and their number of occurrences
#Weight algorithm for recommending tracks
rec_tracks = {}

for i in range(0,k):
    #dist = pred[0][0][i]
    for track in Y["favorite_tracks"][pred[1][0][i]]:
        #TODO: calculate score here
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
