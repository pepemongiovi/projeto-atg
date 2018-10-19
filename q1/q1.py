#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import csv

with open('../spotifyDB.json') as f:
	data = json.load(f)

charset='utf-8'
nodes = {}
edges = []
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

# def setEdges():
# 	global edges
# 	n1 = None
# 	for n2 in nodes:
# 		if(n1==None):
# 			n1 = n2
# 		else:
# 			edge = [n1,n2]
# 			edges.append(edge)
# 			n1 = n2

def generateCSV():
	with open('nodes.csv', mode='w') as nodes_file:
		nodes_writer = csv.writer(nodes_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
		nodes_writer.writerow(['Id', 'Label', 'Weight'])
		for node in nodes:
			nodes_writer.writerow([node,nodes[node][TRACK_NAME_INDEX], nodes[node][TRACK_COUNT_INDEX]])
	
	# with open('edges.csv', mode='w') as edges_file:
	# 	edges_writer = csv.writer(edges_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
	# 	edges_writer.writerow(['Source', 'Target'])
	# 	for edge in edges:
	# 		edges_writer.writerow(edge)
	

def run():
	setNodes()
	# setEdges()
	generateCSV()

run()

