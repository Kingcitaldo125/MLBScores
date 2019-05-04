from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

webAddress = "https://www.baseball-reference.com/boxes/?year=2019&month=05&day=2"

html = urlopen(webAddress)
soup = BeautifulSoup(html,features="html.parser")

data = soup.prettify()
title = data[45471:45585]
scores = str(data[87500:96875])

#print(scores)
splits = ""
for m in re.finditer(r"\S", scores, re.S|re.I):
	#print("")
	splits += m.group()

gameList = splits.split("</div><divclass=\"game_summarynohover\">")
print("GameList:",len(gameList))

for game in gameList:
	mO = re.search(r"loser.+shtml\">(\w+)</a>.+Final.+winner.+shtml\">(\w+)</a>.+<tbody>.+<strong>([A-Z])</strong>.+<td>(\w+[(]\d+-\d+[)])</td>.+<strong>([A-Z])</strong>.+<td>(\w+[(]\d+-\d+[)])</td>.+</tbody>", game, re.S|re.M|re.I)
	if mO:
		print("")
		#print(":",mO.group(0))
		print("Losing Team:",mO.group(1))
		print("Winning Team:",mO.group(2))
		print("Pitcher Result:",mO.group(3))
		print("Pitcher:",mO.group(4))
		print("Pitcher Result:",mO.group(5))
		print("Pitcher:",mO.group(6))
	else:
		mOO = re.search(r"winner.+shtml\">(\w+)</a>.+Final.+loser.+shtml\">(\w+)</a>.+<tbody>.+<strong>([A-Z])</strong>.+<td>(\w+[(]\d+-\d+[)])</td>.+<strong>([A-Z])</strong>.+<td>(\w+[(]\d+-\d+[)])</td>.+</tbody>", game, re.S|re.M|re.I)
		if mOO:
			print("")
			#print(":",mOO.group(0))
			print("Winning Team:",mOO.group(1))
			print("Losing Team:",mOO.group(2))
			print("Pitcher Result:",mOO.group(3))
			print("Pitcher:",mOO.group(4))
			print("Pitcher Result:",mOO.group(5))
			print("Pitcher:",mOO.group(6))
	
	#print(game)
	#print("")
	#print("")
	#print("")
