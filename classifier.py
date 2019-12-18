from sklearn.neighbors import NearestNeighbors
import pandas as pd

X = pd.read_json('./data/popvsrockvsrap.json')
Y = pd.read_json('./data/pop.json')

X_test = [[0.0, 0.0, 1.0]]

knn = NearestNeighbors(n_neighbors=2)
knn.fit(X)
pred = knn.kneighbors(X_test,return_distance=False)

for track in Y["favoriteTracks"][pred[0][0]]:
    if track['genre'] == 'Pop' or track['genre'] == 'Rock' or track['genre'] == 'Hip-hop & Rap':
        print(track['title']  + "     " + str(track['genre']))

