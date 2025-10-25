import gspread
import string
import unicodedata
from datetime import datetime

#this file handles anything regarding google sheets
#we use gspread to interact with google sheets.
#Ideally, this script generates everything from scratch, so if you create a new blank spreadsheet, this script should give and format all data perfectly
#And it does! For the most part. As far as I can tell GSpread does nothing to interact with tables, so that has to be created beforehand, starting on row DATA_ROW for 7 columns and extending for as many rows as there are heroes in HOTS

DATA_ROW = 5 #row where data begins

#returns worksheet we are working with 
def getWorksheet(index = 0):
	gc = gspread.service_account("./gspread/service_account.json")

	ws = gc.open("fenchad spreadsheet").get_worksheet(index)

	return ws

#strip accents from hero names
def stripAccents(text):
	#shamelessly stolen from https://stackoverflow.com/a/4512721
	return ''.join(char for char in
				   unicodedata.normalize('NFKD', text)
				   if unicodedata.category(char) != 'Mn')
				   
#writes data to google sheets
#data should be a map of hero name to an object containing the data of each hero
#"isMaps" is true if we are writing map data
def writeData(data,upToDate,isMaps:bool = False):
	
	ws = getWorksheet(1 if isMaps else 0 )
	
	colLength = len(data)#length of each column, not including the header. Since each stat has one entry per hero, this is number is the number of heroes ever played
	
	if colLength > 1:
		rowLength = len(data[0]) #length of the row, aka how many unique stats we are tracking
		
		cells = ws.range(DATA_ROW,1,colLength + DATA_ROW,rowLength);
		
		#array of formats https://developers.google.com/workspace/sheets/api/reference/rest/v4/spreadsheets/cells#cellformat
		#the way formats are collected is a bit inefficient; I apply a specific format object to each cell, as opposed to applying one format to a whole range, 
		#But since the color of the winrates have to change and are specific to each winrate, I figured it was easier just to assign each cell its own format. 
		#Non-winrate stats definitely could have one format applied to all of them though, same with the header row
		formats = [0]*len(cells)
	   
		col = 0
		
		#collect all the data into cells
		#while we're at it, collect the format of each cell as well
		for key in data[0]: 
			#create header row and format it
			cells[col].value = key
			formats[col] = {"range": gspread.utils.rowcol_to_a1(DATA_ROW,col+1),"format":{"horizontalAlignment":"CENTER","textFormat": {"bold": True}}}
		   
			#add hero stats for each hero 
			for i in range(len(data)):
				index = col + (i + 1)*rowLength
				
				#all data cells have their text centered and have padding of 20 pixels (to make the pics look okay)
				formats[index] = {"range": gspread.utils.rowcol_to_a1(DATA_ROW + i + 1,col+1),\
				"format":{"horizontalAlignment":"CENTER","verticalAlignment":"MIDDLE","padding":{"top":20,"bottom":20,"left":20,"right":20},"textFormat":{"bold":True}}}
				
				#set the value of each cell
				val = data[i][key];
				if key[-2:] == "WR": #winrate data will be rounded to the last 4 decimal places. Configure the table on Google Sheets to have Column Type of Number -> Percent and you got percentages rounded to the nearest two decimal places
					val = int(val*10000)/10000   
					formats[index]["format"]["textFormat"]["foregroundColor"] = {"red":(val < 0.5)*(1 - val),"blue":0.0,"green":min(val,0.7)}
				elif key == "HERO" or key == "MAP": #grab images
					link = ""
					if not isMaps:
						link = "https://www.heroesprofile.com/images/heroes/" + stripAccents(val.lower().translate(str.maketrans('', '', string.punctuation))) + ".png"
					else:
						mapName = val.lower().replace(" ","-")
						link = "https://heroescodex.com/images/maps/" + mapName+ "/" + mapName + "-map.png"
					val = "=image(\"" + link + "\")"
				
				#set value
				cells[index].value = val
				
			col += 1
			
		#write the data and format it
		ws.update_cells(cells, value_input_option='USER_ENTERED')
		ws.batch_format(formats);

		#add the date of the last game that was added
		ws.update_cell(1,1,"up to date as of: " + datetime.fromtimestamp(upToDate).strftime('%Y-%m-%d'))
		ws.format('A1', {'textFormat': {'bold': True,'foregroundColor':{'red':1.0}}})

		


