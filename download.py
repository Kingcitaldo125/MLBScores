from urllib.request import urlopen
from bs4 import BeautifulSoup
from datetime import datetime
import re
import MLBClasses

printScores = False
printResults = True

year = "2019"
month = "05"
day = "15"

intYear = int(year)
if intYear < 1871:
	print("Year cannot be before 1871:setting to 1871")
	intYear = 1871

currYear = datetime.today().year
if intYear > currYear:
	intYear = intYear % currYear

webAddress = "https://www.baseball-reference.com/boxes/?"
webAddress += "year="
webAddress += year
webAddress += "&month="
webAddress += month
webAddress += "&day="
webAddress += day

html = urlopen(webAddress)
soup = BeautifulSoup(html,features="html.parser")

data = soup.prettify()
title = data[45471:45585]
scores = str(data[87500:105500])

if printScores:
	print(scores)

# Date
year = ""
month = ""
day = ""
dMatch = re.match(r"^.+year=(.+).+month=(.+).+day=(.+)", webAddress, re.M|re.I)
if dMatch:
	year = dMatch.group(1)
	month = dMatch.group(2)
	day = dMatch.group(3)

print("Date",year+month+day)

splits = ""
for m in re.finditer(r"\S", scores, re.S|re.I):
	#print("")
	splits += m.group()

gameList = splits.split("</div><divclass=\"game_summarynohover\">")
print("GameList:",len(gameList))

for game in gameList:
	mO = re.search(r"loser.+shtml\">(\w+)</a>.+Final.+winner.+shtml\">(\w+)</a>.+<tbody>.+<strong>([A-Z])</strong>.+<td>(\w+[(]\d+-\d+[)])</td>.+<strong>([A-Z])</strong>.+<td>(\w+[(]\d+-\d+[)])</td>.+</tbody>", game, re.S|re.M|re.I)
	if mO:
		wP = MLBClasses.getPitcherInformation(mO.group(4))
		lP = MLBClasses.getPitcherInformation(mO.group(6))
		winPitch = MLBClasses.Pitcher(wP[0],wP[1])
		losePitch = MLBClasses.Pitcher(lP[0],lP[1])
		if printResults:
			print("")
			print("Winning Team:", MLBClasses.getTeamInformation(mO.group(1)))
			print("Losing Team:", MLBClasses.getTeamInformation(mO.group(2)))
			print("Pitcher Result:",mO.group(3))
			print("Pitcher:",winPitch)
			print("Pitcher Result:",mO.group(5))
			print("Pitcher:",losePitch)
	else:
		mOO = re.search(r"winner.+shtml\">(\w+)</a>.+Final.+loser.+shtml\">(\w+)</a>.+<tbody>.+<strong>([A-Z])</strong>.+<td>(\w+[(]\d+-\d+[)])</td>.+<strong>([A-Z])</strong>.+<td>(\w+[(]\d+-\d+[)])</td>.+</tbody>", game, re.S|re.M|re.I)
		if mOO:
			wP = MLBClasses.getPitcherInformation(mOO.group(4))
			lP = MLBClasses.getPitcherInformation(mOO.group(6))
			winPitch = MLBClasses.Pitcher(wP[0],wP[1])
			losePitch = MLBClasses.Pitcher(lP[0],lP[1])
			if printResults:
				print("")
				print("_Winning Team:", MLBClasses.getTeamInformation(mOO.group(1)))
				print("_Losing Team:", MLBClasses.getTeamInformation(mOO.group(2)))
				print("_Pitcher Result:", mOO.group(3))
				print("_Pitcher:", winPitch)
				print("_Pitcher Result:", mOO.group(5))
				print("_Pitcher:", losePitch)
