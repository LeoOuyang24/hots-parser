from sheets import writeData
from collect import *

#folder with all the replays
gamesFolder = "games"
scrimsFolder = "scrims"

#get game data
gamesData = getData(gamesFolder)
scrimsData = getData(scrimsFolder)

#find last game played
upToDate = max(getNewest(gamesFolder),getNewest(scrimsFolder))

#combine scrims and games data
totalData = compileData(scrimsData,gamesData)
        
#write that shit to google sheets;
writeData(totalData,upToDate)
