#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import csv
from operator import itemgetter

with open('../spotifyDB.json') as f:
	data = json.load(f)

charset='utf-8'
artistsNodes = {}
artistsEdges = []
playlistsNodes = []
playlistsEdges = []
ARTIST_ID_INDEX = 0
ARTIST_NAME_INDEX = 1

def setArtistsNodes():
	global artistsNodes
	i = 1

	for p in data["playlists"]:
		for m in p["tracks"]:
			if(artistsNodes.get(m["artist_name"])==None):
				artistsNodes[m["artist_name"]] = [i, m["artist_name"].encode(charset)]
				i+=1


def getAmountOfPlaylistInCommon(artistName1, artistName2):
	commonPlaylists = 0

	for p in data["playlists"]:
		hasArtist1 = False
		hasArtist2 = False

		for m in p["tracks"]:
			if(m["artist_name"].lower()==artistName1.lower()):
				hasArtist1 = True
			if(m["artist_name"].encode(charset).lower()==artistName2.lower()):
				hasArtist2 = True

		if(hasArtist1 and hasArtist2):
			commonPlaylists+=1

	return commonPlaylists


def getSelectedArtistIndex(selectedArtistName):
	selectedArtistIndex = None

	for artistName in artistsNodes:
		if(artistName.lower()==selectedArtistName.lower()):
			selectedArtistIndex = artistsNodes[artistName][ARTIST_ID_INDEX]

	return selectedArtistIndex

def getArtistNameById(artistId):
	for artistName in artistsNodes:
		if(artistId==artistsNodes[artistName][ARTIST_ID_INDEX]):
			return artistsNodes[artistName][ARTIST_NAME_INDEX]


def setArtistsEdges(selectedArtistName, selectedArtistIndex):
	global artistsEdges

	for artistName in artistsNodes:
		if(artistsNodes[artistName][ARTIST_NAME_INDEX].lower()!=selectedArtistName.lower()):
			playlistsInCommon = getAmountOfPlaylistInCommon(selectedArtistName, artistsNodes[artistName][ARTIST_NAME_INDEX])
			
			if(playlistsInCommon>0):
				edge = [selectedArtistIndex, artistsNodes[artistName][ARTIST_ID_INDEX], playlistsInCommon]
				artistsEdges.append(edge)

# def setPlaylistsEdges():
# 	global playlistsEdges
# 	for i in range (len(playlistsNodes)):
# 		for j in range (i+1,len(playlistsNodes)):
# 			edge = [playlistsNodes[i][0], playlistsNodes[j][0]]
# 			playlistsEdges.append(edge)

def generateCSV():
	with open('artistsNodes.csv', mode='w') as nodes_file:
		nodes_writer = csv.writer(nodes_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
		nodes_writer.writerow(['Id', 'Label'])
		for node in artistsNodes:
			nodes_writer.writerow(artistsNodes[node])

	with open('artistsEdges.csv', mode='w') as edges_file:
		edges_writer = csv.writer(edges_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
		edges_writer.writerow(['Source', 'Target', 'Weight'])
		for edge in artistsEdges:
			edges_writer.writerow(edge)

	with open('playlistsNodes.csv', mode='w') as nodes_file:
		nodes_writer = csv.writer(nodes_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
		nodes_writer.writerow(['Id', 'Label', 'Weight'])
		for node in playlistsNodes:
			nodes_writer.writerow(node)

	# with open('playlistsEdges.csv', mode='w') as edges_file:
	# 	edges_writer = csv.writer(edges_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
	# 	edges_writer.writerow(['Source', 'Target'])
	# 	for edge in playlistsEdges:
	# 		edges_writer.writerow(edge)


def getMostSimilarArtists():
	NUM_OF_ARTISTS = 5
	mostSimilarArtists = []
	sortedEdges = sorted(artistsEdges,key=itemgetter(2))

	for i in range(-1,-NUM_OF_ARTISTS-1,-1):
		artistIndex = getArtistNameById(sortedEdges[i][1])
		mostSimilarArtists.append(artistIndex)

	return mostSimilarArtists


def setPlaylistsNodes(selectedArtistName, mostSimilarArtists):
	global playlistsNodes
	i = 1

	for p in data["playlists"]:
		counter = 0

		for m in p["tracks"]:
			if(m["artist_name"].lower() == selectedArtistName.lower()):
				counter = 0
				break
			if(m["artist_name"].encode(charset) in mostSimilarArtists):
				counter+=1

		node = [p["pid"], p["name"].encode(charset), counter]
		playlistsNodes.append(node)

def printResult(mostSimilarArtists):
	print "Most similar artists: " + ', '.join(mostSimilarArtists)
	print 'pid of recomended playlist: ' + str(sorted(playlistsNodes,key=itemgetter(2))[-1][0])

def run():
	selectedArtistName = raw_input("Insira o nome do artista: ")
	setArtistsNodes()
	selectedArtistIndex = getSelectedArtistIndex(selectedArtistName)

	if(selectedArtistIndex==None):
		print "Artista não encontrado!"
	else:
		setArtistsEdges(selectedArtistName, selectedArtistIndex)
		mostSimilarArtists = getMostSimilarArtists()
		setPlaylistsNodes(selectedArtistName, mostSimilarArtists)
		# setPlaylistsEdges()
		printResult(mostSimilarArtists)
		generateCSV()

run()
		

