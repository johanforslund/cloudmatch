import requests
import time
import json

client_id = 'cEIhboHJ92pcRNyYQhmg5gYgL69kQlrM'
current_genre = 'pop'

result = []

params = { 'limit' : '200', 'genres': current_genre }

tracks = requests.get('https://api.soundcloud.com/tracks?client_id=' + client_id, params).json()
track = tracks[-1]

params = {'limit': '200', 'linked_partitioning': '1'}

track_properties = ('id', 'likes_count', 'comment_count', 'genre', 'permalink_url', 'title', 'description', 'streamable', 'stream_url')

favoriters = requests.get('https://api.soundcloud.com/tracks/' + str(track['id']) + '/favoriters?client_id=' + client_id, params).json()

for i in range(0, 2):
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
            favorite_track_info = {}
            favorite_track_info['track_id'] = favorite_track['id']
            favorite_track_info['likes_count'] = favorite_track['likes_count']
            favorite_track_info['comment_count'] = favorite_track['comment_count']
            favorite_track_info['genre'] = favorite_track['genre']
            favorite_track_info['permalink_url'] = favorite_track['permalink_url']
            favorite_track_info['title'] = favorite_track['title']
            favorite_track_info['description'] = favorite_track['description']
            favorite_track_info['streamable'] = favorite_track['streamable']
            favorite_track_info['stream_url'] = favorite_track['stream_url']
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
