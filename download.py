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

done = False
while not done:
	displayMenu()
	retCode = listenForOptions()
	if retCode == 0:
		done = True
