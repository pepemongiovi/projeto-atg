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

def setNodes():
	global nodes
	for p in data["playlists"]:
		for m in p["tracks"]:
			if(nodes.get(m["track_uri"])==None):
				nodes[m["track_uri"]] = [1, m["track_name"].encode(charset)]
			else:
				nodes[m["track_uri"]][0] += 1 		

def generateCSV():
	with open('nodes.csv', mode='w') as nodes_file:
		nodes_writer = csv.writer(nodes_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
		nodes_writer.writerow(['track_uri', 'track_name', 'weight'])

		for node in nodes:
			nodes_writer.writerow([node,nodes[node][TRACK_NAME_INDEX], nodes[node][TRACK_COUNT_INDEX]])
	

def run():
	setNodes()
	generateCSV()

run()

