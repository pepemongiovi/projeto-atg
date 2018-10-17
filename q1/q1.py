#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import csv

with open('../spotifyDB.json') as f:
	data = json.load(f)

charset='utf-8'
nodes = {}
TRACK_COUNT_INDEX = 0
TRACK_NAME_INDEX = 1

for p1 in data["playlists"]:
	for m in p1["tracks"]:
		if(nodes.get(m["track_uri"])==None):
			nodes[m["track_uri"]] = [1, m["track_name"].encode(charset)]
		else:
			nodes[m["track_uri"]][0] += 1 		

with open('nodes.csv', mode='w') as nodes_file:
	nodes_writer = csv.writer(nodes_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
	nodes_writer.writerow(['id', 'name', 'weight'])
	i = 1
	for node in nodes:
		nodes_writer.writerow([i,nodes[node][TRACK_NAME_INDEX], nodes[node][TRACK_COUNT_INDEX]])
		i+=1

