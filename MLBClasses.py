import re

class Pitcher(object):
	def __init__(self, name, record="(?,?)"):
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
	print("pString", pString)
	mRes = re.match(r'(.+)([(].+[)])',pString, re.I | re.M)
	name = ""
	record = ""
	if mRes:
		name = getTeamInformation(mRes.group(1))
		record = mRes.group(2)
	else: # could not get record for pitcher
		mRes = re.match(r'(.+)',pString, re.I | re.M)
		if mRes:
			name = getTeamInformation(mRes.group(1))
			return name
			
	return [name,record]

def getGameInformation(game, saveProg, winTeamO, looseTeamO, winPitch, losePitch, printResults, AwayWinner):
	saveO = saveProg.search(game)
	if printResults:
		print("")
		if AwayWinner:
			print("W", getTeamInformation(winTeamO.group(1)), winTeamO.group(2))
			print(getTeamInformation(looseTeamO.group(1)), looseTeamO.group(2))
		else:
			print(getTeamInformation(looseTeamO.group(1)), looseTeamO.group(2))
			print("W", getTeamInformation(winTeamO.group(1)), winTeamO.group(2))
		print("\t", "W", winPitch)
		print("\t", "L", losePitch)
		if saveO:
			sName = getTeamInformation(saveO.group(1))
			sRecord = None
			sRecord = saveO.group(2)
			if sRecord == None:
				info = sName + " " + "(?)"
				print("\t S", sName)
			else:
				info = sName + " " + sRecord
				print("\t S", info)
