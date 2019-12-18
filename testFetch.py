import requests
import time
import json

client_id = 'cEIhboHJ92pcRNyYQhmg5gYgL69kQlrM'
current_genre = 'rock'

result = []

params = { 'limit' : '200', 'genres': current_genre }

tracks = requests.get('https://api.soundcloud.com/tracks?client_id=' + client_id, params).json()
track = tracks[-1]

params = {'limit': '200', 'linked_partitioning': '1'}

track_properties = ('id', 'likes_count', 'comment_count', 'genre', 'permalink_url', 'title', 'stream_url')

favoriters = requests.get('https://api.soundcloud.com/tracks/' + str(track['id']) + '/favoriters?client_id=' + client_id, params).json()

for i in range(0, 25):
    print(i)
    if 'collection' not in favoriters.keys():
        break

    for favoriter in favoriters['collection']:
        user = {'user_id': favoriter['id']}
        favorite_tracks = requests.get('https://api.soundcloud.com/users/' + str(favoriter['id']) + '/favorites?client_id=' + client_id, {'limit': '200'})

        if favorite_tracks:
            favorite_tracks = favorite_tracks.json()
        else:
            break

        favorite_tracks_list = []

        for favorite_track in favorite_tracks:
            if not all (k in favorite_track for k in track_properties):
                continue
            favorite_track_info = {k: favorite_track[k] for k in track_properties}
            favorite_tracks_list.append(favorite_track_info)

        user['favorite_tracks'] = favorite_tracks_list

        result.append(user)

        time.sleep(0.5)

    if 'next_href' not in favoriters.keys():
        break

    next_href = favoriters['next_href']
    favoriters = requests.get(next_href).json()

with open('./data/' + current_genre + '.json', 'w', encoding='utf8') as json_file:
    json.dump(result, json_file, ensure_ascii=False)
