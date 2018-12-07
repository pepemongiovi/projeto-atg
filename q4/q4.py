#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Pergunta: Playlists colaborativas tendem a ser mais ecléticas? 

import json
import csv

with open('../spotifyDB.json') as f:
	data = json.load(f)

charset='utf-8'
nodes = []
edges = []

def setNodes():
	global nodes
	for p in data["playlists"]:
		nodes.append(p)

def setEdges():
	global edges
	for i in range(len(nodes)):
		playlist1 = nodes[i]
		for j in range(i+1, len(nodes)):
			playlist2 = nodes[j]
			if(playlist1["collaborative"] == playlist2["collaborative"]):
				edge = [playlist1["pid"], playlist2["pid"]]
				edges.append(edge)

def getNumberOfDiffArtistsInPlaylist(playlist):
	artists = []
	for track in playlist["tracks"]:
		artist = track["artist_uri"]
		if(artist not in artists):
			artists.append(artist)
	return len(artists)

def generateCSV():
	with open('nodes.csv', mode='w') as nodes_file:
		nodes_writer = csv.writer(nodes_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
		nodes_writer.writerow(['Id', 'Collaborative','DistinctArtists'])
		for node in nodes:
			distinctArtists = getNumberOfDiffArtistsInPlaylist(node)
			row = [ node["pid"], node["collaborative"], distinctArtists ]
			nodes_writer.writerow(row)

	with open('edges.csv', mode='w') as edges_file:
		edges_writer = csv.writer(edges_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
		edges_writer.writerow(['Source', 'Target'])
		for edge in edges:
			edges_writer.writerow(edge)

def run():
	setNodes()
	setEdges()
	generateCSV()
run()