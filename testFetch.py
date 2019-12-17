import requests
import time
import json

client_id = 'cEIhboHJ92pcRNyYQhmg5gYgL69kQlrM'
currentGenre = 'pop'
params = { 'limit' : '200', 'genres': currentGenre }
tracks = requests.get('https://api.soundcloud.com/tracks?client_id=' + client_id, params).json()

result = []

track = tracks[-1]
params = {'limit': '200', 'linked_partitioning': '1'}

favoriters = requests.get('https://api.soundcloud.com/tracks/' + str(track['id']) + '/favoriters?client_id=' + client_id, params).json()

params = {'limit': '200'}

trackProperties = ('id', 'likes_count', 'reposts_count', 'genre', 'permalink_url', 'title', 'description', 'streamable', 'stream_url')

for i in range(0, 1):
    if 'next_href' not in favoriters.keys() or 'collection' not in favoriters.keys():
        break

    next_href = favoriters['next_href']
    favoriters = requests.get(next_href).json()

    for favoriter in favoriters['collection']:
        user = {'user_id': favoriter['id']}
        favoriteTracks = requests.get('https://api.soundcloud.com/users/' + str(favoriter['id']) + '/favorites?client_id=' + client_id, params)
        if favoriteTracks:
            favoriteTracks = favoriteTracks.json()
        else:
            break

        favoriteTracksList = []

        for favoriteTrack in favoriteTracks:
            if not all (k in favoriteTrack for k in trackProperties):
                continue
            favoriteTrackInfo = {}
            favoriteTrackInfo['track_id'] = favoriteTrack['id']
            favoriteTrackInfo['likes_count'] = favoriteTrack['likes_count']
            favoriteTrackInfo['reposts_count'] = favoriteTrack['reposts_count']
            favoriteTrackInfo['genre'] = favoriteTrack['genre']
            favoriteTrackInfo['permalink_url'] = favoriteTrack['permalink_url']
            favoriteTrackInfo['title'] = favoriteTrack['title']
            favoriteTrackInfo['description'] = favoriteTrack['description']
            favoriteTrackInfo['streamable'] = favoriteTrack['streamable']
            favoriteTrackInfo['stream_url'] = favoriteTrack['stream_url']
            favoriteTracksList.append(favoriteTrackInfo)

        user['favoriteTracks'] = favoriteTracksList

        result.append(user)
    break

with open('./data/' + currentGenre + '.json', 'w', encoding='utf8') as json_file:
    json.dump(result, json_file, ensure_ascii=False)
