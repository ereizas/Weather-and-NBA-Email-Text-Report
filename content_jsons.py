from datetime import date, timedelta
import requests
import keys_and_passwords
yesterday = str(date.today()-timedelta(days = 1))
url = "https://www.balldontlie.io/api/v1/games?start_date=" +yesterday + "&end_date=" + yesterday
response = requests.get(url)
scoresJSON = response.json()
teamsPlayed = [[]]
scores = [[]]
#index for teamsPlayed and scores
i = 0
if scoresJSON['data']!=[]:
    #goes through all elememts since the two team are in separate dictionaries in the larger dictionary for each game
    for a in range(len(scoresJSON["data"])):
        if(teamsPlayed[i]!=[] and scores[i]!=[]):
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


url = "https://www.balldontlie.io/api/v1/games?start_date=" +str(date.today()) + "&end_date=" + str(date.today())
response = requests.get(url)
scheduleJSON = response.json()

'''def 
apiKey = keys_and_passwords.apiKey
units = ["imperial","metric","standard"]
response = requests.get("https://api.openweathermap.org/data/2.5/onecall?lat=" + c[0] + "&lon=" + c[1] + "&units="+units[unitsInd]+"&exclude=minutely,daily&appid="+apiKey)
forecastJSON = response.json()'''