import requests
import time
import json

client_id = 'csSEELZJ9CZQAJnUIssLDhWdk2oSkPC9'
currentGenre = 'rock'
params = { 'limit' : '20', 'genres': currentGenre }
tracks = requests.get('https://api.soundcloud.com/tracks?client_id=' + client_id, params).json()

result = []

for count, track in enumerate(tracks):
    params = {'limit': '200', 'linked_partitioning': '1'}

    favoriters = requests.get('https://api.soundcloud.com/tracks/' + str(track['id']) + '/favoriters?client_id=' + client_id, params).json()

    for i in range(0, 500):
        if 'next_href' not in favoriters.keys() or 'collection' not in favoriters.keys():
            break

        next_href = favoriters['next_href']
        favoriters = requests.get(next_href).json()

        favoritersIds = ([favoriter['id'] for favoriter in favoriters['collection']])
        
        if i%10 == 0:
            print('Inner loop: ' + str(i))


    trackInfo = {}
    trackInfo['id'] = track['id']
    trackInfo['genre'] = track['genre']
    trackInfo['playback_count'] = track['playback_count']
    trackInfo['favoritings_count'] = track['favoritings_count']
    trackInfo['favoriters'] = favoritersIds
    result.append(trackInfo)
    print('Outer loop: ' + str(count))
    time.sleep(0.05)


with open(currentGenre + '.json', 'w', encoding='utf8') as json_file:
    json.dump(result, json_file, ensure_ascii=False)