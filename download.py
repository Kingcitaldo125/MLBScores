# Copyright (c) 2021 Paul Arelt
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# Test Dates: 2019-6-3
from urllib.request import urlopen
from bs4 import BeautifulSoup
from datetime import datetime
import re
import MLBClasses

printData = False
printResults = True

# Menu function
def displayMenu():
	print("\n**************************************")
	print("Select an Option Below:\n")
	print("1:Get yesterday's scores")
	print("2:Get tomorrow's scores (coming soon)")
	print("3:Get scores for a particular date")
	print("4:Exit")
	print("**************************************\n")
	
# Option listener function
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

def getDate(webAddress):
	year = ""
	month = ""
	day = ""
	dMatch = re.match(r"^.+year=(.+).+month=(.+).+day=(.+)", webAddress, re.M|re.I)
	if dMatch:
		year = dMatch.group(1)
		month = dMatch.group(2)
		day = dMatch.group(3)

	monthDict = {1:"Jan", 2:"Feb", 3:"Mar", 4:"Apr", 5:"May", 6:"Jun", 7:"Jul", 8:"Aug", 9:"Sep", 10:"Oct", 11:"Nov", 12:"Dec"}
	newdt = datetime.strptime(monthDict[int(month)]+" "+day+" "+year, "%b %d %Y")
	print("Date", newdt.strftime("%b %d %Y"))

# Main function
def main(year,month,day):
	intYear = int(year)
	# No baseball before 1871
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

	# Concatenate the URL containing the information
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
	lowerLimit = 86885
	upperLimit = 115900
	
	# Trim the end of the list of games down
	# Helps compile times for the final game
	# in the list of games
	buff = ""
	word = ""
	start = 0
	trigger = False
	for dd in range(lowerLimit,upperLimit):
		word += data[dd]
		if data[dd] == "\n":
			if "filter switcher" in word:
				trigger = True
			word = ""
		if trigger:
			start += 1
	upperLimit -= (start+0) # for good measure
	scores = str(data[lowerLimit:upperLimit])

	if printData:
		print(scores)

	# Date
	getDate(webAddress)

	splits = ""
	for m in re.finditer(r"\S", scores, re.S|re.I):
		#print("")
		splits += m.group()

	if printData:
		print("splits", splits)
	gameList = splits.split("<divclass=\"game_summarynohover\">")
	#print("gameList", gameList)
	print("GameList:",len(gameList)-1)
	
	
	if len(gameList) == 1: # check for no games played
		m = re.match(r'^.*<h3>(\w+)</h3>.*$', gameList[0], re.I|re.M)
		if m:
			print("No Games Were or Have Yet Been Played on This Date")
			return
		
		
	winProg = re.compile(r"loser.+shtml\">.+winner.+shtml\">(\w+[.]+\w+|\w+)+</a>.+\"right\">(\d+)</td>.+</tr>", re.S|re.M|re.I)
	looseProg = re.compile(r"loser.+shtml\">(\w+[.]+\w+|\w+)+</a>.+\"right\">(\d+)</td>.+winner", re.S|re.M|re.I)
	
	_winProg = re.compile(r"winner.+shtml\">(\w+[.]+\w+|\w+)+</a>.+\"right\">(\d+)</td>.+loser", re.S|re.M|re.I)
	_looseProg = re.compile(r"winner.+shtml\">.+loser.+shtml\">(\w+[.]+\w+|\w+)+</a>.+\"right\">(\d+)</td>.+</tr>", re.S|re.M|re.I)
	
	pitchRegex = r"<table><tbody><tr><td><strong>W</strong></td><td>([A-Z.]+)([(]\d+[-]\d+[)])?</td></tr><tr><td><strong>L</strong></td><td>([A-Z.]+)([(]\d+[-]\d+[)])?</td></tr>.+</div>"
	saveRegex = r"<strong>S</strong></td><td>([A-Z.]+)([(]\d+[)])?</td></tr></tbody></table>"
	pitchProg = re.compile(pitchRegex, re.S|re.M|re.I)
	saveProg = re.compile(saveRegex, re.S|re.M|re.I)
	
	# Iterate through the list of games that have whitespace trimmed
	# matching against the regex patterns listed above
	# After matching for one or the other, extract information using regex groups
	for game in gameList:
		if game == '':
			continue
		#print("Game", game)
		looseTeamO = looseProg.search(game)
		winTeamO = winProg.search(game)
		#print("WinTeamO", winTeamO)
		#print("LooseTeamO", looseTeamO)
		pitchO = pitchProg.search(game)
		#print("PitchO", pitchO)
		if looseTeamO and winTeamO and pitchO: # try to match on one type of regex pattern pair - Home team won
			wPName = pitchO.group(1)
			wPRecord = None
			wPRecord = pitchO.group(2)
			wP = [MLBClasses.getTeamInformation(wPName), wPRecord if wPRecord is not None else "(?,?)"]
			#print("wP",wP)
			
			lPName = pitchO.group(3)
			lPRecord = None
			lPRecord = pitchO.group(4)
			lP = [MLBClasses.getTeamInformation(lPName), lPRecord if lPRecord is not None else "(?,?)"]
			#print("lP",lP)
			
			# Handle cases where pitcher(s) don't have W-L records
			winPitch = None
			losePitch = None
			if isinstance(wP,str):
				winPitch = MLBClasses.Pitcher(wP)
			else:
				winPitch = MLBClasses.Pitcher(wP[0], wP[1])
			
			if isinstance(lP,str):
				losePitch = MLBClasses.Pitcher(lP)
			else:
				losePitch = MLBClasses.Pitcher(lP[0], lP[1])
			
			MLBClasses.getGameInformation(game, saveProg, winTeamO, looseTeamO, winPitch, losePitch, printResults, False)

		else: # try another regex pattern pair - Away team won
			_winTeamO = _winProg.search(game)
			_looseTeamO = _looseProg.search(game)
			pitchO = pitchProg.search(game)
			if _looseTeamO and _winTeamO and pitchO: # try to match on one type of regex pattern pair
				_wPName = pitchO.group(1)
				_wPRecord = pitchO.group(2)
				_wP = [MLBClasses.getTeamInformation(_wPName), _wPRecord  if _wPRecord is not None else "(?,?)"]
				#print("wP",_wP)
				
				_lPName = pitchO.group(3)
				_lPRecord = pitchO.group(4)
				_lP = [MLBClasses.getTeamInformation(_lPName), _lPRecord if _lPRecord is not None else "(?,?)"]
				#print("lP",_lP)
			
				# Handle cases where pitcher(s) don't have W-L records
				_winPitch = None
				_losePitch = None
				if isinstance(_wP,str):
					_winPitch = MLBClasses.Pitcher(_wP)
				else:
					_winPitch = MLBClasses.Pitcher(_wP[0], _wP[1])
				
				if isinstance(_lP,str):
					_losePitch = MLBClasses.Pitcher(_lP)
				else:
					_losePitch = MLBClasses.Pitcher(_lP[0], _lP[1])
				
				MLBClasses.getGameInformation(game, saveProg, _winTeamO, _looseTeamO, _winPitch, _losePitch, printResults, True)

done = False
while not done:
	displayMenu()
	retCode = listenForOptions()
	if retCode == 0:
		done = True
