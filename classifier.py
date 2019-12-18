from sklearn.neighbors import NearestNeighbors
import pandas as pd

X = pd.read_json('./data/popvsrockvsrap.json')
Y = pd.read_json('./data/pop.json')

X_test = [[0.0, 0.0, 1.0]]

knn = NearestNeighbors(n_neighbors=2)
knn.fit(X)
pred = knn.kneighbors(X_test)

#TODO: add dictionary with track_ids and their number of occurrences
#Weight algorithm for recommending tracks
rec_tracks = {}

for i in range(0,2):
    dist = pred[0][0][i]
    for track in Y["favorite_tracks"][pred[1][0][i]]:
        #TODO: calculate score here
        if track['track_id'] in rec_tracks:
            rec_tracks[track['track_id']] -= track['likes_count'] / 2000000.0
        else:
            rec_tracks[track['track_id']] = track['likes_count'] / 1000000.0

maxScore = {'track_id': 0, 'score': 0}

for track in rec_tracks:
    if rec_tracks[track] > maxScore['score']:
        maxScore['score'] = rec_tracks[track]
        maxScore['track_id'] = track

print(maxScore)