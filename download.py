'''
Copyright (c) 2021 Paul Arelt
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

download.py
'''

# Test Dates: 2019-6-3

import json
import re

from urllib.request import urlopen
from datetime import datetime
from bs4 import BeautifulSoup

import MLBClasses

print_data = False
print_results = True

do_export_json = False

# Menu function
def display_menu():
    '''display_menu'''
    print("\n**************************************")
    print("Select an Option Below:\n")
    print("1:Get yesterday's scores")
    print("2:Get tomorrow's scores (coming soon)")
    print("3:Get scores for a particular date")
    print("4:Exit")
    print("**************************************\n")

# Option listener function
def listen_for_options():
    '''listen_for_options'''
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

def get_date(web_address):
    '''get_date'''
    year = ""
    month = ""
    day = ""
    dMatch = re.match(r"^.+year=(.+).+month=(.+).+day=(.+)", web_address, re.M|re.I)
    if dMatch:
        year = dMatch.group(1)
        month = dMatch.group(2)
        day = dMatch.group(3)

    monthDict = {1:"Jan", 2:"Feb", 3:"Mar", 4:"Apr", 5:"May", 6:"Jun", 7:"Jul",
	    8:"Aug", 9:"Sep", 10:"Oct", 11:"Nov", 12:"Dec"}
    newdt = datetime.strptime(monthDict[int(month)]+" "+day+" "+year, "%b %d %Y")
    print("Date", newdt.strftime("%b %d %Y"))

def export_json(win_team_o, loose_team_o, win_pitch, wp_record, lose_pitch, lp_record, home_team_won):
    games_json = []
    if export_json:
        game_json = None
        if home_team_won:
            game_json = {"teams":{"loose":{"name":"", "score":"", "pitcher":{"name":"", "record":""}}, "win":{"name":"", "score":"", "pitcher":{"name":"", "record":""}}}}
        else:
            game_json = {"teams":{"win":{"name":"", "score":"", "pitcher":{"name":"", "record":""}}, "loose":{"name":"", "score":"", "pitcher":{"name":"", "record":""}}}}

        game_json['teams']['win']['name'] = MLBClasses.getTeamInformation(win_team_o.group(1))
        game_json['teams']['win']['score'] = win_team_o.group(2)

        game_json['teams']['loose']['name'] = MLBClasses.getTeamInformation(loose_team_o.group(1))
        game_json['teams']['loose']['score'] = loose_team_o.group(2)

        game_json['teams']['win']['pitcher']['name'] = win_pitch.getName()
        game_json['teams']['win']['pitcher']['record'] = wp_record

        game_json['teams']['loose']['pitcher']['name'] = lose_pitch.getName()
        game_json['teams']['loose']['pitcher']['record'] = lp_record

        games_json.append(game_json)

    return games_json

# Main function
def main(year,month,day):
    '''main'''
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
    web_address = "https://www.baseball-reference.com/boxes/?"
    web_address += "year="
    web_address += year
    web_address += "&month="
    web_address += month
    web_address += "&day="
    web_address += day

    html = urlopen(web_address)
    soup = BeautifulSoup(html,features="html.parser")

    data = soup.prettify()
    # title = data[45471:45585]
    lower_limit = 86885
    upper_limit = 115920

    # Trim the end of the list of games down
    # Helps compile times for the final game
    # in the list of games
    word = ""
    start = 0
    trigger = False
    for dd in range(lower_limit,upper_limit):
        word += data[dd]
        if data[dd] == "\n":
            if "filter switcher" in word:
                trigger = True
            word = ""
        if trigger:
            start += 1
    upper_limit -= (start+0) # for good measure
    scores = str(data[lower_limit:upper_limit])

    if print_data:
        print(scores)

    # Date
    get_date(web_address)

    splits = ""
    for m in re.finditer(r"\S", scores, re.S|re.I):
        splits += m.group()

    if print_data:
        print("splits", splits)
    game_list = splits.split("<divclass=\"game_summarynohover\">")
    #print("game_list", game_list)
    print("game_list:",len(game_list)-1)


    if len(game_list) == 1: # check for no games played
        m = re.match(r'^.*<h3>(\w+)</h3>.*$', game_list[0], re.I|re.M)
        if m:
            print("No Games Were or Have Yet Been Played on This Date")
            return


    win_prog = re.compile(
	    r"loser.+shtml\">.+winner.+shtml\">(\w+[.]+\w+|\w+)+</a>.+\"right\">(\d+)</td>.+</tr>",
	    re.S|re.M|re.I)
    loose_prog = re.compile(
	    r"loser.+shtml\">(\w+[.]+\w+|\w+)+</a>.+\"right\">(\d+)</td>.+winner",
	    re.S|re.M|re.I)

    _win_prog = re.compile(
	    r"winner.+shtml\">(\w+[.]+\w+|\w+)+</a>.+\"right\">(\d+)</td>.+loser",
	    re.S|re.M|re.I)
    _loose_prog = re.compile(
	    r"winner.+shtml\">.+loser.+shtml\">(\w+[.]+\w+|\w+)+</a>.+\"right\">(\d+)</td>.+</tr>",
	    re.S|re.M|re.I)

    pitch_regex = r"<table><tbody><tr><td><strong>W</strong></td><td>([A-Z-.áéíúüñÁÉÍÓÚÜÑ]+)([(]\d+[-]\d+[)])?</td></tr><tr><td><strong>L</strong></td><td>([A-Z-.áéíúüñÁÉÍÓÚÜÑ]+)([(]\d+[-]\d+[)])?</td></tr>.+</div>"
    save_regex = r"<strong>S</strong></td><td>([A-Z.]+)([(]\d+[)])?</td></tr></tbody></table>"
    pitch_prog = re.compile(pitch_regex, re.S|re.M|re.I)
    save_prog = re.compile(save_regex, re.S|re.M|re.I)

    # Iterate through the list of games that have whitespace trimmed
    # matching against the regex patterns listed above
    # After matching for one or the other, extract information using regex groups
    games_json = []
    for game in game_list:
        if game == '':
            continue
        #print("Game", game)
        loose_team_o = loose_prog.search(game)
        win_team_o = win_prog.search(game)
        #print("win_team_o", win_team_o)
        #print("loose_team_o", loose_team_o)
        pitch_o = pitch_prog.search(game)
        #print("pitch_o", pitch_o)

        # try to match on one type of regex pattern pair - Home team won
        if loose_team_o and win_team_o and pitch_o:
            wp_name = pitch_o.group(1)
            wp_record = None
            wp_record = pitch_o.group(2)
            wP = [MLBClasses.getTeamInformation(wp_name),
			    wp_record if wp_record is not None else "(?,?)"]
            #print("wP:",wP)

            lp_name = pitch_o.group(3)
            lp_record = None
            lp_record = pitch_o.group(4)
            lP = [MLBClasses.getTeamInformation(lp_name),
			    lp_record if lp_record is not None else "(?,?)"]
            #print("lP:",lP)

            # Handle cases where pitcher(s) don't have W-L records
            win_pitch = None
            lose_pitch = None
            if isinstance(wP,str):
                win_pitch = MLBClasses.Pitcher(wP)
            else:
                win_pitch = MLBClasses.Pitcher(wP[0], wP[1])

            if isinstance(lP,str):
                lose_pitch = MLBClasses.Pitcher(lP)
            else:
                lose_pitch = MLBClasses.Pitcher(lP[0], lP[1])

            MLBClasses.getGameInformation(game,
			    save_prog,
			    win_team_o,
			    loose_team_o,
			    win_pitch,
			    lose_pitch,
			    print_results,
			    False)

            # Fill in JSON struct information
            if do_export_json:
                for game in export_json(win_team_o, loose_team_o, win_pitch, wp_record, lose_pitch, lp_record, True):
                    games_json.append(game)

        else: # try another regex pattern pair - Away team won
            _win_team_o = _win_prog.search(game)
            _loose_team_o = _loose_prog.search(game)
            pitch_o = pitch_prog.search(game)
            # try to match on one type of regex pattern pair
            if _loose_team_o and _win_team_o and pitch_o:
                _wp_name = pitch_o.group(1)
                _wp_record = pitch_o.group(2)
                _wP = [MLBClasses.getTeamInformation(_wp_name),
                    _wp_record  if _wp_record is not None else "(?,?)"]
                #print("wP:",_wP)

                _lp_name = pitch_o.group(3)
                _lp_record = pitch_o.group(4)
                _lP = [MLBClasses.getTeamInformation(_lp_name),
                    _lp_record if _lp_record is not None else "(?,?)"]
                #print("lP:",_lP)

                # Handle cases where pitcher(s) don't have W-L records
                _win_pitch = None
                _lose_pitch = None
                if isinstance(_wP,str):
                    _win_pitch = MLBClasses.Pitcher(_wP)
                else:
                    _win_pitch = MLBClasses.Pitcher(_wP[0], _wP[1])

                if isinstance(_lP,str):
                    _lose_pitch = MLBClasses.Pitcher(_lP)
                else:
                    _lose_pitch = MLBClasses.Pitcher(_lP[0], _lP[1])

                MLBClasses.getGameInformation(game,
                    save_prog,
                    _win_team_o,
                    _loose_team_o,
                    _win_pitch,
                    _lose_pitch,
                    print_results,
                    True)

                # Fill in JSON struct information
                if do_export_json:
                    for game in export_json(_win_team_o, _loose_team_o, _win_pitch, _wp_record, _lose_pitch, _lp_record, False):
                        games_json.append(game)
    if do_export_json:
        with open('out.json','w') as f:
            json.dump(games_json, f, indent=2)

done = False
while not done:
    display_menu()
    retcode = listen_for_options()
    if retcode == 0:
        done = True
