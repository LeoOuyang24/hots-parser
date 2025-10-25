import sys
import shutil
import math
import argparse
import sys
import json
import mpyq
import pprint

#add all the libaries we need
#if we don't do this hero_cli can't find the debuggers
sys.path.append("D:\\NGS\\potential replays\\heroprotocol")

from heroprotocol.heroprotocol import hero_cli
from heroprotocol.heroprotocol.versions import build, latest
import os


#This file handles all HOTS data. Everything here should work without locally without internet access

fensad = ["Ruglord","RobotWizard","Atd09","Psyqo","JazzyFast","JazzyVal","FenixEnjoyer"]


#get replay details
#input is a path to a replay file
#output is a json object
def getDetails(path):
    # Read the protocol header, this can be read with any protocol
    archive = mpyq.MPQArchive(path)

    contents = archive.header['user_data_header']['content']
    header = latest().decode_replay_header(contents)

    # The header's baseBuild determines which protocol to use
    baseBuild = header['m_version']['m_baseBuild']
    try:
        protocol = build(baseBuild)
    except:
        print('Unsupported base build: %d' % baseBuild, file=sys.stderr)
        sys.exit(1)   

    contents = archive.read_file('replay.details')
    details = protocol.decode_replay_details(contents)
    return details

#get hero and map data from a folder
#returns a mapping of hero/map to a dictionary of data 
# data["heroes"][hero name] -> {"wins": int, "games": int}
# data["maps"][map name] -> {"wins": int, "games": int}
def getData(folderPath):
	heroData = {}
	mapData = {}
	data = {}
	# Get the list of all files in a directory
	files = os.listdir(folderPath)
	newestFileTime = -1;
	#for each file
	for file in files:
		fullPath = folderPath +"/" + file
		try:
			deets = getDetails(fullPath) #get the details
			won = None
			for key in deets["m_playerList"]: #for each hero in that game...
					if key["m_name"].decode("utf-8") in fensad:
						#figure out if we won, dependent on the first fensad member in the party's results (so if we ever do inhouses this wont work)
						if won == None:
							won = key["m_result"] == 1

						hero = key["m_hero"].decode("utf-8") 
						if hero not in heroData:
							heroData[hero] = {"wins": 0, "games": 0}

						heroData[hero]["wins"] += won
						heroData[hero]["games"] += 1
		   	
		   	#map specific data
			mapName = deets["m_title"].decode("utf-8")
			if mapName not in mapData:
				mapData[mapName] = {"wins":0,"games":0}
			mapData[mapName]["wins"] += (won)
			mapData[mapName]["games"] += 1
		except Exception as error:
			print("Error parsing " + fullPath + ": " + str(error))

	data["heroes"] = heroData
	data["maps"] = mapData;
	return data
	   		
#get latest replay time in unix
def getNewest(folderPath):
    newestFileTime = -1;
    #for each file
    files = os.listdir(folderPath)
    for file in files:
        fullPath = folderPath +"/" + file
        if os.path.getmtime(fullPath) > newestFileTime:
            newestFileTime = os.path.getmtime(fullPath)   
    return newestFileTime

#given scrims data and games data, compiles it into one big array
#input data should be a map of hero/map names to data
#output is an array of objects:
#   "HERO_NAME": hero name, "MAP_NAME" if isMaps is true 
#   "HERO": hero name again (for the hero pic), "MAP" if isMaps is true
#   "SCRIMS WR": scrim win rate (percentage)
#   "SCRIM GAMES": number of scrim games 
#   "MATCHES WR": win rate in matches (percentage)
#   "MATCH GAMES": number of matches played
#   "TOTAL WR": total win rate across scrims and matches (percentage)
#   "TOTAL GAMES": total number of games played between scrims and matches
def compileData(scrimsData,gamesData,isMaps:bool = False):
	totalData = []
	for heroes in set(list(scrimsData.keys()) + list(gamesData.keys())):
		name = ("HERO_NAME" if not isMaps else "MAP_NAME")
		label = ("HERO" if not isMaps else "MAP")
		totalData.append({name: heroes,label: heroes,"SCRIMS WR": 0, "SCRIM GAMES": 0, "MATCHES WR": 0, "MATCH GAMES": 0, "TOTAL WR": 0,"TOTAL GAMES":0})
		if heroes in scrimsData:
			totalData[-1]["SCRIMS WR"] = scrimsData[heroes]["wins"]/scrimsData[heroes]["games"]
			totalData[-1]["SCRIM GAMES"] = scrimsData[heroes]["games"]
			totalData[-1]["TOTAL GAMES"] += scrimsData[heroes]["games"]
			totalData[-1]["TOTAL WR"] += scrimsData[heroes]["wins"]
		if heroes in gamesData:
			totalData[-1]["MATCHES WR"] = gamesData[heroes]["wins"]/gamesData[heroes]["games"]
			totalData[-1]["MATCH GAMES"] = gamesData[heroes]["games"]
			totalData[-1]["TOTAL GAMES"] += gamesData[heroes]["games"]
			totalData[-1]["TOTAL WR"] += gamesData[heroes]["wins"]
		totalData[-1]["TOTAL WR"] = totalData[-1]["TOTAL WR"]/totalData[-1]["TOTAL GAMES"]
	return totalData
