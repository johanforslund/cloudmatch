import json
from flask import Flask, request, redirect, g, render_template
from flask_cors import CORS, cross_origin
import requests
import pandas as pd
import numpy as np
import re
import ijson
from urllib.parse import quote
from sklearn.neighbors import NearestNeighbors
import classifier
import config


# Authentication Steps, paramaters, and responses are defined at https://developer.spotify.com/web-api/authorization-guide/
# Visit this url to see all the steps, parameters, and expected response.

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

#  Client Keys
CLIENT_ID = config.CLIENT_ID
CLIENT_SECRET = config.CLIENT_SECRET

# Spotify URLS
SPOTIFY_AUTH_URL = "https://accounts.spotify.com/authorize"
SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
SPOTIFY_API_BASE_URL = "https://api.spotify.com"
API_VERSION = "v1"
SPOTIFY_API_URL = "{}/{}".format(SPOTIFY_API_BASE_URL, API_VERSION)

# Server-side Parameters
CLIENT_SIDE_URL = "http://localhost"
PORT = 3000
REDIRECT_URI = "{}:{}/tracks/callback".format(CLIENT_SIDE_URL, PORT)
SCOPE = "playlist-modify-public playlist-modify-private user-top-read"
STATE = ""
SHOW_DIALOG_bool = True
SHOW_DIALOG_str = str(SHOW_DIALOG_bool).lower()

auth_query_parameters = {
    "response_type": "code",
    "redirect_uri": REDIRECT_URI,
    "scope": SCOPE,
    # "state": STATE,
    # "show_dialog": SHOW_DIALOG_str,
    "client_id": CLIENT_ID
}

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

X = pd.read_json('../data/splitAll3.json')
print("Finished reading split")
#Y = parse_data('./data/combined.json')
Y = parse_data('../data/combined.json')
print("Finished reading data")

genres = pd.read_json('../data/genres.json')['genres']
genres = genres.values.tolist()

k = 128


@app.route("/")
def index():
    # Auth Step 1: Authorization
    url_args = "&".join(["{}={}".format(key, quote(val)) for key, val in auth_query_parameters.items()])
    auth_url = "{}/?{}".format(SPOTIFY_AUTH_URL, url_args)
    return redirect(auth_url)


@app.route("/callback/q")
def callback():
    # Auth Step 4: Requests refresh and access tokens
    access_token = request.args['access_token']

    # Auth Step 6: Use the access token to access Spotify API
    authorization_header = {"Authorization": "Bearer {}".format(access_token)}
    params = {"limit": "50"}

    # Get profile data
    user_profile_api_endpoint = "{}/me/top/artists".format(SPOTIFY_API_URL)
    profile_response = requests.get(user_profile_api_endpoint, params=params, headers=authorization_header)
    profile_data = json.loads(profile_response.text)

    print(profile_data)

    # Combine profile and playlist data to display
    display_arr = [profile_data]

    list_of_genres = [a['genres'] for a in profile_data['items']]
    
    BB = []
    CC = []

    for ll in list_of_genres:
        LL = list(set(ll))
        for kk in LL:
            BB.append(kk.split())
        CC.append(BB)
        BB = []

    flat_genres = [item2 for sublist in CC for item in sublist for item2 in item]

    numOfGenres = len(genres)

    mean_genre = [0] * numOfGenres
    for genre in flat_genres:
        genre = clean_genre(genre)
        try:
            idx = genres.index(genre)
        except ValueError:
            continue
        mean_genre[idx] += 1

    normalizer = sum(mean_genre)
    if normalizer == 0:
        normalizer = 1
    for i in range(0,len(mean_genre)):
        mean_genre[i] = mean_genre[i] / normalizer
    clf = classifier.Classifier(genres, k)
    maxScores, pred = clf.classify(mean_genre, X, Y)

    result = []

    for j in range(0, 10):
        for i in range(0,k):
            for track in Y[1][pred[1][0][i]]:
                if track['id'] == maxScores[j][0]:
                    #print(track['permalink_url'])
                    #print(maxScores[j][1])
                    #print(track['id'])
                    #print(track['genre'])
                    result.append(track['stream_url'])
                    break

    return {"data": result}


if __name__ == "__main__":
    app.run(debug=True, port=8080)
