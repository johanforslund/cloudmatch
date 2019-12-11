import requests
import time
import json

client_id = 'csSEELZJ9CZQAJnUIssLDhWdk2oSkPC9'
currentGenre = 'rock'
params = { 'limit' : '50', 'genres': currentGenre }
tracks = requests.get('https://api.soundcloud.com/tracks?client_id=' + client_id, params).json()

result = []
favoritersIds = []

for track in tracks:
    params = {'limit': '200', 'linked_partitioning': '1'}

    favoriters = requests.get('https://api.soundcloud.com/tracks/' + str(track['id']) + '/favoriters?client_id=' + client_id, params).json()

    for i in range(0, 10):
        if 'next_href' not in favoriters.keys():
            break
        next_href = favoriters['next_href']
        favoriters = requests.get(next_href).json()

        favoritersIds = favoritersIds + ([favoriter['id'] for favoriter in favoriters['collection']])
        print(i)

    trackInfo = {}
    trackInfo['id'] = track['id']
    trackInfo['genre'] = track['genre']
    trackInfo['favoriters'] = favoritersIds
    result.append(trackInfo)
    time.sleep(0.05)


with open('output.json', 'w', encoding='utf8') as json_file:
    json.dump(result, json_file, ensure_ascii=False)