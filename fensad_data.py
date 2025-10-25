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
totalHeroData = compileData(scrimsData["heroes"],gamesData["heroes"])
totalMapsData = compileData(scrimsData["maps"],gamesData["maps"])        

#write that shit to google sheets;
writeData(totalHeroData,upToDate)
writeData(totalMapsData,upToDate,True)
