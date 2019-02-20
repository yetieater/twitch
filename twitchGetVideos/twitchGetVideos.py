import twitchID
import requests, json
import pandas as pd
import datetime
import subprocess
import sys

clientId = twitchID.clientId

headers = {'Client-ID': clientId}

# mode selector - choose between full and short
## full returns everything
## short returns a single page of results
mode = 'short'
type = 'archive'

def getVideos(userId='80562408', n='100', type='archive', cursor=None):
	# type=archive
	# type=highlight
	# type=upload
	if cursor is not None:
		url = 'https://api.twitch.tv/helix/videos?user_id=' + userId + '&first=' + n + '&type=' + type + '&after=' + cursor
	else:
		url = 'https://api.twitch.tv/helix/videos?user_id=' + userId + '&first=' + n + '&type=' + type
	return requests.get(url, headers=headers)

def parseResponse(response):
	if response.status_code == 200:
		json = response.json()
		if len(json['pagination']) == 0:
			cursor = "Fin"
		else:
			cursor = json['pagination']['cursor']
		return json, cursor
	else:
		print("Uh oh!")
		print(response.status_code)
		print(response.text)

def jsonToDataframe(json):
	#return pd.DataFrame.from_dict(json['data'])
	return pd.DataFrame.from_dict(json)

def request(url, headers=headers):
	return requests.get(url, headers=headers)

# test_api_url = 'https://api.twitch.tv/helix/videos?user_id=' + userId + '&first=' + n + '&type=' + type + '&after=' + cursor

jsonData = []

if mode == "full":
	cursor = None
	while cursor != "Fin":
		response = getVideos(type=type, cursor=cursor)
		json, cursor = parseResponse(response)
		jsonData += json['data']
elif mode == "short":
	response = getVideos()
	json, cursor = parseResponse(response)
	jsonData += json['data']

df = jsonToDataframe(jsonData)

# created_at values look like '2019-02-10T22:31:51Z'

# Fields of Interest
fieldsOfInterest = ['created_at', 'duration', 'id', 'title']

dfFOI = df[fieldsOfInterest]

# Output
dfFOI.to_csv(path_or_buf="getVideos" + '-' + type + '-' + mode + '-' + str(datetime.datetime.now()))