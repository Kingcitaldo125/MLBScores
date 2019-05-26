from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

class Pitcher(object):
	def __init__(self, name, record):
		self.name = name
		self.record = record
	
	def __str__(self):
		retStr = ""
		retStr += self.name
		retStr += " "
		retStr += self.record
		return retStr
	
	def getAsString(self):
		retStr = ""
		retStr += self.name
		retStr += " "
		retStr += self.record
		return retStr

class GameResult(object):
	def __init__(self, winnerTeam, loserTeam, pitcherWinner, pitcherLoser):
		self.winnerTeam = winnerTeam
		self.loserTeam = loserTeam
		self.pitcherWinner = pitcherWinner
		self.pitcherLoser = pitcherLoser
		
	def __str__(self):
		retStr = ""
		retStr += self.winnerTeam
		retStr += ","
		retStr += self.loserTeam
		retStr += ","
		retStr += self.pitcherWinner
		retStr += ","
		retStr += self.pitcherLoser0
		return retStr
	
	def getWinningTeam(self):
		return self.winnerTeam
	
	def getLosingTeam(self):
		return self.loserTeam
	
	def getWinningPitcher(self):
		return self.pitcherWinner
	
	def getLosingPitcher(self):
		return self.pitcherLoser
		
def getTeamInformation(tString):
	resTString = ""
	pos = 0
	for t in tString:
		if pos > 0 and (t >= 'A' and t <= 'Z'):
			resTString += " "
		resTString += t
		pos += 1

	return resTString

def getPitcherInformation(pString):
	mRes = re.match(r'(\w+)(\(.+\))',pString, re.I | re.M)
	name = ""
	record = ""
	if mRes:
		#print("Pitcher Info:",mRes.group(0))
		name = getTeamInformation(mRes.group(1))
		record = mRes.group(2)
	return [name,record]

webAddress = "https://www.baseball-reference.com/boxes/?year=2019&month=05&day=2"

html = urlopen(webAddress)
soup = BeautifulSoup(html,features="html.parser")

data = soup.prettify()
title = data[45471:45585]
scores = str(data[87500:96875])

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
		wP = getPitcherInformation(mO.group(4))
		lP = getPitcherInformation(mO.group(6))
		winPitch = Pitcher(wP[0],wP[1])
		losePitch = Pitcher(lP[0],lP[1])
		print("")
		print("Winning Team:", getTeamInformation(mO.group(1)))
		print("Losing Team:", getTeamInformation(mO.group(2)))
		print("Pitcher Result:",mO.group(3))
		print("Pitcher:",winPitch)
		print("Pitcher Result:",mO.group(5))
		print("Pitcher:",losePitch)
	else:
		mOO = re.search(r"winner.+shtml\">(\w+)</a>.+Final.+loser.+shtml\">(\w+)</a>.+<tbody>.+<strong>([A-Z])</strong>.+<td>(\w+[(]\d+-\d+[)])</td>.+<strong>([A-Z])</strong>.+<td>(\w+[(]\d+-\d+[)])</td>.+</tbody>", game, re.S|re.M|re.I)
		if mOO:
			wP = getPitcherInformation(mOO.group(4))
			lP = getPitcherInformation(mOO.group(6))
			winPitch = Pitcher(wP[0],wP[1])
			losePitch = Pitcher(lP[0],lP[1])
			print("")
			print("_Winning Team:", getTeamInformation(mOO.group(1)))
			print("_Losing Team:", getTeamInformation(mOO.group(2)))
			print("_Pitcher Result:", mOO.group(3))
			print("_Pitcher:", winPitch)
			print("_Pitcher Result:", mOO.group(5))
			print("_Pitcher:", losePitch)
