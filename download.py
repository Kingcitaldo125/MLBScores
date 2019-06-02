from urllib.request import urlopen
from bs4 import BeautifulSoup
from datetime import datetime
import re
import MLBClasses

printScores = False
printResults = True

def displayMenu():
	print("\n*************************")
	print("Select an Option Below:\n")
	print("1:Get yesterday's scores")
	print("2:Get tomorrow's scores (coming soon)")
	print("3:Get scores for a particular date")
	print("4:Exit")
	print("*************************\n")
	
def listenForOptions():
	option = str(input(''))
	if option == "1":
		year = str(datetime.today().year)
		month = str(datetime.today().month)
		day = str(datetime.today().day)
		print("Yesterday's Scores:")
		main(year,month,str((int(day)-1)))
	elif option == "2":
		print("Coming Soon")
	elif option == "3":
		print("Enter in Year")
		year = str(input(''))
		print("Enter in Month")
		month = str(input(''))
		print("Enter in Day")
		day = str(input(''))
		print("Scores for "+year+month+day+":")
		main(year,month,day)
	elif option == "4":
		return 0
	else:
		print("Cannot get information for the current option")
	
	return 1

def main(year,month,day):
	intYear = int(year)
	if intYear < 1871:
		print("Year cannot be before 1871:setting to 1871")
		intYear = 1871

	currYear = datetime.today().year
	if intYear > currYear:
		intYear = currYear
	
	intMonth = int(month)
	if intMonth > 12:
		intMonth = 12
	if intMonth < 1:
		intMonth = 1
		
	intDay = int(day)
	if intDay > 31:
		intDay = 31
	if intDay < 1:
		intDay = 1
	
	year = str(intYear)
	month = str(intMonth)
	day = str(intDay)

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
	scores = str(data[87500:105900])

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

	winProg = re.compile(r"<tbody>.+loser.+shtml\">.+winner.+shtml\">(\w+[.]+\w+|\w+)+</a>.+\"right\">(\d+)</td>.+</tr>", re.S|re.M|re.I)
	looseProg = re.compile(r"<tbody>.+loser.+shtml\">(\w+[.]+\w+|\w+)+</a>.+\"right\">(\d+)</td>.+</tr>.+winner", re.S|re.M|re.I)
	
	_winProg = re.compile(r"<tbody>.+winner.+shtml\">(\w+[.]+\w+|\w+)+</a>.+\"right\">(\d+)</td>.+</tr>.+loser", re.S|re.M|re.I)
	_looseProg = re.compile(r"<tbody>.+winner.+shtml\">.+loser.+shtml\">(\w+[.]+\w+|\w+)+</a>.+\"right\">(\d+)</td>.+</tr>", re.S|re.M|re.I)
	
	pitchProg = re.compile(r"<table><tbody>.+<strong>([A-Z])</strong>.+<td>(\w+\(\d+-\d+\))</td>.+<strong>([A-Z])</strong>.+<td>(\w+[(]\d+-\d+[)])</td>.+</tbody></table>", re.S|re.M|re.I)
	for game in gameList:
		looseTeamO = looseProg.search(game)
		winTeamO = winProg.search(game)
		pitchO = pitchProg.search(game)
		if looseTeamO and winTeamO and pitchO: # try to match on one type of regex pattern pair - Home team won
			wP = MLBClasses.getPitcherInformation(pitchO.group(2))
			lP = MLBClasses.getPitcherInformation(pitchO.group(4))
			winPitch = MLBClasses.Pitcher(wP[0],wP[1])
			losePitch = MLBClasses.Pitcher(lP[0],lP[1])
			if printResults:
				print("")
				print(MLBClasses.getTeamInformation(looseTeamO.group(1)), looseTeamO.group(2))
				print("W", MLBClasses.getTeamInformation(winTeamO.group(1)), winTeamO.group(2))
				print("\t", pitchO.group(1), winPitch)
				print("\t", pitchO.group(3), losePitch)
				
		else: # try another regex pattern pair - Away team won
			_winTeamO = _winProg.search(game)
			_looseTeamO = _looseProg.search(game)
			pitchO = pitchProg.search(game)
			if _looseTeamO and _winTeamO and pitchO: # try to match on one type of regex pattern pair
				_wP = MLBClasses.getPitcherInformation(pitchO.group(2))
				_lP = MLBClasses.getPitcherInformation(pitchO.group(4))
				_winPitch = MLBClasses.Pitcher(_wP[0],_wP[1])
				_losePitch = MLBClasses.Pitcher(_lP[0],_lP[1])
				if printResults:
					print("")
					print("W", MLBClasses.getTeamInformation(_winTeamO.group(1)), _winTeamO.group(2))
					print(MLBClasses.getTeamInformation(_looseTeamO.group(1)), _looseTeamO.group(2))
					print("\t", pitchO.group(1), _winPitch)
					print("\t", pitchO.group(3), _losePitch)


done = False
while not done:
	displayMenu()
	retCode = listenForOptions()
	if retCode == 0:
		done = True
