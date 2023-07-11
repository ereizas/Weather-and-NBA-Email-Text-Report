from datetime import date, timedelta
import requests
import keys_and_passwords
import csv
#collection of JSON info for yesterday's NBA scores
yesterday = str(date.today()-timedelta(days = 1))
url = "https://www.balldontlie.io/api/v1/games?start_date=" +yesterday + "&end_date=" + yesterday
response = requests.get(url)
scoresJSON = response.json()
#index for teamsPlayed and scores
i = 0
teamsPlayed = [[]]
if scoresJSON['data']!=[]:
    scores = [[]]
    #goes through all elememts since the two team are in separate dictionaries in the larger dictionary for each game
    for a in range(len(scoresJSON["data"])):
        if teamsPlayed[i]!=[] and scores[i]!=[]:
            i+=1
            teamsPlayed.append([])
            scores.append([])
        for b in scoresJSON['data'][a]:
            if b=='home_team_score' and scoresJSON['data'][a][b]==0:
                continue
            elif b=='visitor_team_score' and scoresJSON['data'][a][b]==0:
                continue
            elif b == "home_team":
                teamsPlayed[i].append(scoresJSON['data'][a]['home_team']['name'])
            elif b == 'home_team_score':
                scores[i].append(scoresJSON['data'][a][b])
            elif b == "visitor_team":
                teamsPlayed[i].append(scoresJSON['data'][a]['visitor_team']['name'])
            elif b == "visitor_team_score":
                scores[i].append(scoresJSON['data'][a][b])
if teamsPlayed[0]==[]:
    teamsPlayed=[]
#collection of JSON info for today's NBA schedule
url = "https://www.balldontlie.io/api/v1/games?start_date=" +str(date.today()) + "&end_date=" + str(date.today())
response = requests.get(url)
scheduleJSON = response.json()
i=0
teamsPlaying = [[]]
if scheduleJSON['data']!=[]:
    playTimes = [0]
    for a in range(len(scheduleJSON["data"])):
        if teamsPlaying[i]!=[] and playTimes[i]!=0:
            teamsPlaying.append([])
            playTimes.append(0)
            i+=1
        for b in scheduleJSON['data'][a]:
            if b=='home_team_score' and scheduleJSON['data'][a][b]==0:
                pass
            elif b=='visitor_team_score' and scheduleJSON['data'][a][b]==0:
                pass
            elif b == "home_team":
                teamsPlaying[i].append(scheduleJSON['data'][a]['home_team']['name'])
            elif b =="status":
                playTimes[i] = scheduleJSON['data'][a]['status']
            elif b == "visitor_team":
                teamsPlaying[i].append(scheduleJSON['data'][a]['visitor_team']['name'])
if teamsPlaying[0]==[]:
    teamsPlaying=[]
#Extracting of zipcodes from ZIP,LAT,LNG.csv
#csv file from Eric Hurst at https://gist.github.com/erichurst/7882666
file = open("ZIP,LAT,LNG.csv")
csvreader = csv.reader(file)
rows = []
for line in csvreader:
    rows.append(line)
#removes the first line
rows = rows[1:]
file.close()