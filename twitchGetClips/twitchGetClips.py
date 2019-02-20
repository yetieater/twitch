import twitchID
import requests, json
import pandas as pd
import datetime

import subprocess
import sys

clientId = twitchID.clientId
broadcasterId = '80562408'

headers = {'Client-ID': clientId}

def getClips(broadcasterId=broadcasterId, n='100', cursor=None):
	# started_at
	# ended_at
	if cursor is not None:
		url = 'https://api.twitch.tv/helix/clips?broadcaster_id=' + broadcasterId + '&first=' + n + '&after=' + cursor
	else:
		url = 'https://api.twitch.tv/helix/clips?broadcaster_id=' + broadcasterId + '&first=' + n
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

jsonData = []
cursor = None
while cursor != "Fin":
	response = getClips(cursor=cursor)
	json, cursor = parseResponse(response)
	jsonData += json['data']
df = jsonToDataframe(jsonData)

# All Fields
# broadcaster_id,broadcaster_name,created_at,creator_id,creator_name,embed_url,game_id,id,language,thumbnail_url,title,url,video_id,view_count

# Fields of Interest
fieldsOfInterest = ['created_at', 'creator_name', 'id', 'title']
# embed_url,game_id,id,language,thumbnail_url,url,view_count

# dfFOI = df[fieldsOfInterest]

# Output
df.to_csv(path_or_buf="getClips" + str(datetime.datetime.now()))
# dfFOI.to_csv(path_or_buf=str(datetime.datetime.now()))
