from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

webAddress = "https://www.baseball-reference.com/boxes/?year=2019&month=05&day=2"

html = urlopen(webAddress)
soup = BeautifulSoup(html,features="html.parser")

data = soup.prettify()
title = data[45471:45585]
scores = data[87560:95500]

#print("Title:",title)
#print("Scores:",scores)

regx = r"loser(.+)winner(.+)"
#WinPitcherRegex = r"W\s+(.+)\s+\((\d+-\d+)\)"
#LoosePitcherRegex = r"L\s+(.+)\s+\((\d+-\d+)\)"

mObj = re.search(regx, scores, re.S|re.I|re.M)
if mObj:
	#print("Group 0:", mObj.group(0))
	print("Group 1:", mObj.group(1))
	print("Group 2:", mObj.group(2))
	
	
