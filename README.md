# MLB Game Results (MLBScores)
## Get the results from any regular season MLB game in MLB history (1871 onwards)

Special thanks to [Baseball Reference](https://www.baseball-reference.com/), which has a de-facto API that makes this possible.
This is essentially a [MUD](https://en.wikipedia.org/wiki/MUD) based on the [boxscores](https://www.baseball-reference.com/boxes/) for Baseball Reference.

## Usage
Follow the command prompt guide for the `download.bat` script like so:

```
**************************************
Select an Option Below:

1:Get yesterday's scores
2:Get tomorrow's scores (coming soon)
3:Get scores for a particular date
4:Exit
**************************************
```

For option ``3``, this can be entered like so:

```
Enter in Year
2001
Enter in Month
4
Enter in Day
1
```

Which will result in:

```
Scores for 200141:
Date Apr 01 2001
```

with a gamelist for all games played.
If there were no games played for that day, it will report:

```
GameList: 0
No Games Were or Have Yet Been Played on This Date
```

### JSON Results
To get the games/scores for a day in JSON format, change the `do_export_json` variable to `True` in the `download.py` file.
Game results will be written to disk after the program finishes parsing game information for a particular date.
