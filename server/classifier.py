from sklearn.neighbors import NearestNeighbors
import numpy as np
import pandas as pd
import re
import ijson

def parse_data(filename):
        data = []
        with open(filename, 'rb') as f:
            for item in ijson.items(f, 'item'):
                data.append(item)
        return pd.DataFrame(data)


def clean_genre(s):
    #TODO: also remove "and" and switch "raphiphop" to "hiphoprap"
    regex = re.compile('[^a-zA-Z]')
    s = regex.sub('', s)
    return s.lower()

class Classifier:
    def __init__(self, genres, k):
        self.genres = genres
        self.k = k

    def classify(self, mean_genre, X, Y):
        X_test = [mean_genre]
        x = np.array(X_test)
        user_genres = np.where(x != 0)[1]
        liked_genres = [self.genres[i] for i in user_genres]

        #X_test = np.random.dirichlet(np.ones(126), size=1)

        #X_test = [ran.random() for i in range(1,127)]
        #s = sum(X_test)
        #X_test = [i/s for i in X_test]
        #X_test = [X_test]

        knn = NearestNeighbors(n_neighbors=self.k)

        knn.fit(X)
        pred = knn.kneighbors(X_test)
        #print(X_test)
        #print("Pred")
        #print(pred)
        #TODO: add dictionary with track_ids and their number of occurrences
        #Weight algorithm for recommending tracks
        rec_tracks = {}

        for i in range(0,self.k):
            #dist = pred[0][0][i]
            for track in Y[1][pred[1][0][i]]:
                #TODO: calculate score here
                #TODO: filter podcast and live

                if not track['genre']:
                    continue
                elif clean_genre(track['genre']) not in liked_genres:
                    continue
                if any(word in track['title'].lower() for word in ['podcast', 'part', 'live']):
                    continue
                if track['likes_count'] > 5000:
                    continue
                if track['comment_count'] < 3:
                    continue
                if track['id'] in rec_tracks:
                    genre = clean_genre(track['genre'])
                    genreIndex = self.genres.index(genre)
                    rec_tracks[track['id']] += 1 + 0.25*X_test[0][genreIndex]
                else:
                    rec_tracks[track['id']] = 1

        maxScores = sorted(rec_tracks.items(), key=lambda x: x[1], reverse=True)

        return maxScores, pred
