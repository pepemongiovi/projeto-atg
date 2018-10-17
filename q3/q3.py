#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import csv

with open('spotifyDB.json') as f:
	data = json.load(f)

charset='utf-8'
nodes = []
edges = []
i = 1

for p1 in data["playlists"]:
	node = [i, p1["name"].encode(charset)]
	j = 1
	for p2 in data["playlists"]:
		if(j>i):
			edge = [i, j]
			counter = 0
			for m1 in p1["tracks"]:
				for m2 in p2["tracks"]:
					if(m1["track_uri"]==m2["track_uri"]):
						counter += 1
			if(counter > 0):
				edge.append(counter)
			edges.append(edge)
		j+=1
	nodes.append(node)
	i+=1

with open('nodes.csv', mode='w') as nodes_file:
	nodes_writer = csv.writer(nodes_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
	nodes_writer.writerow(['id', 'name'])
	for node in nodes:
		print node
		nodes_writer.writerow(node)

with open('edges.csv', mode='w') as edges_file:
	edges_writer = csv.writer(edges_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
	edges_writer.writerow(['source', 'target', 'weight'])
	for edge in edges:
		edges_writer.writerow(edge)