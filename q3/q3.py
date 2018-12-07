#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Pergunta: Dado uma playlist, qual seria uma playlist recomendada levando em consideração as músicas presentes?

import json
import csv

with open('../spotifyDB.json') as f:
	data = json.load(f)

charset='utf-8'
nodes = []
edges = []

def getSelectedPlaylist(pid):
	for p in data["playlists"]:
		if(p["pid"]==pid):
			return p
	return None

def setNodes():
	global nodes
	for p in data["playlists"]:
		nodes.append(p)

def setEdges(selectedPlaylist):
	global edges
	for n in nodes:
		if(n["pid"]!=selectedPlaylist["pid"]):
			counter = 0
			for m1 in n["tracks"]:
				for m2 in selectedPlaylist["tracks"]:
					if(m1["track_uri"]==m2["track_uri"]):
						counter+=1
			edge = [selectedPlaylist["pid"], n["pid"], counter]
			edges.append(edge)
	

def generateCSV():
	with open('nodes.csv', mode='w') as nodes_file:
		nodes_writer = csv.writer(nodes_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
		nodes_writer.writerow(['Id', 'Label'])
		for node in nodes:
			nodes_writer.writerow([node["pid"], node["name"].encode(charset)])

	with open('edges.csv', mode='w') as edges_file:
		edges_writer = csv.writer(edges_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
		edges_writer.writerow(['Source', 'Target', 'Weight'])
		for edge in edges:
			edges_writer.writerow(edge)

def run():
	selectedPlaylistPID = int(raw_input("Insira o pid da playlist: "))
	selectedPlaylist = getSelectedPlaylist(selectedPlaylistPID)
	if(selectedPlaylist==None):
		print "Playlist não encontrada!"
	else:
		setNodes()
		setEdges(selectedPlaylist)
		generateCSV()

run()