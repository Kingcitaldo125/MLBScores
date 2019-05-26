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
