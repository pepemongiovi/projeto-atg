#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import csv

with open('../spotifyDB.json') as f:
	data = json.load(f)

charset='utf-8'
nodes = []

selectedSongUri = raw_input("Insira o uri da música: ")
selectedSongArtist = None

for p in data["playlists"]:
	for m in p["tracks"]:
		if(m["track_uri"]==selectedSongUri):
			selectedSongArtist = m["artist_name"]

if(selectedSongArtist==None):
	print "Música não encontrada!"
else:
	i = 1
	for p in data["playlists"]:
		counter = 0
		for m in p["tracks"]:
			if(m["artist_name"]==selectedSongArtist):
				counter+=1

		node = [i, p["name"].encode(charset), counter]
		nodes.append(node)
		i+=1

	with open('nodes.csv', mode='w') as nodes_file:
		nodes_writer = csv.writer(nodes_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
		nodes_writer.writerow(['id', 'name', 'weight'])
		for node in nodes:
			nodes_writer.writerow(node)
