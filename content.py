#remove unused imports when finished
from datetime import date, timedelta
import time
#from requests.api import get
import requests
import csv

def getScores(teams):
	yesterday = str(date.today()-timedelta(days = 1))
	url = "https://www.balldontlie.io/api/v1/games?start_date=" +yesterday + "&end_date=" + yesterday
	response = requests.get(url)
	data=response.json()
	teamsPlayed = []
	scores = []
	#makes sure to not crash when there were no games played the day before
	if data['data']!=[]:
		#goes through all elememts since the two team are in separate dictionaries in the larger dictionary for each game
		for a in range(len(data["data"])):
			tempTeamPair = []
			tempScorePair = []
			for b in data['data'][a]:
				if b=='home_team_score' and data['data'][a][b]==0:
					pass
				elif b=='visitor_team_score' and data['data'][a][b]==0:
					pass
				elif b == "home_team":
					tempTeamPair.append(data['data'][a]['home_team']['name'])
				elif b == 'home_team_score':
					tempScorePair.append(data['data'][a][b])
				elif b == "visitor_team":
					tempTeamPair.append(data['data'][a]['visitor_team']['name'])
				elif b == "visitor_team_score":
					tempScorePair.append(data['data'][a][b])
					if (tempTeamPair[0] in teams or tempTeamPair[1] in teams) :
						teamsPlayed.append(tempTeamPair[0])
						teamsPlayed.append(tempTeamPair[1])
						scores.append(tempScorePair[0])
						scores.append(tempScorePair[1])

		res = "Yesterday's Scores: \n"
		for t in range(1,len(teamsPlayed),2):
			if scores[t-1]>scores[t]:
				res += teamsPlayed[t-1] + " beat " + teamsPlayed[t] + " " + str(scores[t-1]) + "-" + str(scores[t]) + "\n\n"
			elif scores[t]>scores[t-1]:
				res += teamsPlayed[t] + " beat " + teamsPlayed[t-1] + " " + str(scores[t]) + "-" + str(scores[t-1]) + "\n\n"
		if res =="Yesterday's Scores: \n":
			return "*Your teams did not play any games yesterday.\n\n\n\n\n"
		res+="*If you see that a game that you expected is not shown, then that game has been postponed.\n\n\n\n\n"
		return res
	else:
		return "*No NBA games were played yesterday.\n\n\n\n\n"

#print(getScores(["76ers","Bulls","Trail Blazers","Raptors","Bucks","Nets","Suns"]))

def getSchedule(teams):
	url = "https://www.balldontlie.io/api/v1/games?start_date=" +str(date.today()) + "&end_date=" + str(date.today())
	response = requests.get(url)
	data=response.json()
	teamsPlaying = []
	playTimes = []

	if data['data']!=[]:
		for a in range(len(data["data"])):
			tempTeamPair = []
			timeTemp = ''
			for b in data['data'][a]:
				if b=='home_team_score' and data['data'][a][b]==0:
					pass
				elif b=='visitor_team_score' and data['data'][a][b]==0:
					pass
				elif b == "home_team":
					tempTeamPair.append(data['data'][a]['home_team']['name'])
				elif b =="status":
					timeTemp = data['data'][a]['status']
				elif b == "visitor_team":
					tempTeamPair.append(data['data'][a]['visitor_team']['name'])
					if (tempTeamPair[0] in teams or tempTeamPair[1] in teams) :
						teamsPlaying.append(tempTeamPair[0])
						teamsPlaying.append(tempTeamPair[1])
						playTimes.append(timeTemp)

		res = "Today's Slate: \n"
		for s in range(1,len(teamsPlaying),2):
			res+= teamsPlaying[s-1] + " at " + teamsPlaying[s] + " " + playTimes[int(s/2)] + "\n\n"
		if res == "Today's Slate: \n":
			return "*Your teams are not playing any games today.\n\n\n\n\n"
		return res + "\n\n\n\n\n"
						
	else:
		return "*There are no NBA Games scheduled for today.\n\n\n\n\n"

#print(getSchedule(["76ers","Bulls","Trail Blazers","Raptors","Bucks","Nets","Suns"]))

def getHourlyForecast(unitsInd,zipcodes):
	#csv file from Eric Hurst at https://gist.github.com/erichurst/7882666
	file = open("ZIP,LAT,LNG.csv")
	csvreader = csv.reader(file)
	rows = []
	for line in csvreader:
		rows.append(line)
	#removes the first line
	rows = rows[1:]
	file.close()

	#makes sure that any illegitamate zipcodes are removed so that the binary search while loop doesn't become infinite
	allZips = [i[0] for i in rows]
	legitZipLst = [(j in allZips) for j in zipcodes]
	if not all(legitZipLst):
		for i in range(len(zipcodes)-1,-1,-1):
			if not legitZipLst[i]:
				zipcodes.remove(zipcodes[i])
		print(zipcodes)

	coord = [[] for i in zipcodes]
	#checks if csv file is sorted according to zip code integer order from smallest to largest and it is confirmed true
	"""for r in range(1,len(rows)):
		if int(rows[r][0])<int(rows[r-1][0]):
			print("f")"""
	
	for z in range(len(zipcodes)):
		left = 0
		middle = int(len(rows)/2)
		right = len(rows)
		while(coord[z]==[]):
			#print(zipcodes[z])
			#print(rows[middle][0])
			if int(zipcodes[z])==int(rows[middle][0]):
				coord[z].append(rows[middle][1].strip())
				coord[z].append(rows[middle][2].strip())
				break
			elif left==right:
				coord[z].append(rows[middle][1].strip())
				coord[z].append(rows[middle][2].strip())
				break
			elif int(zipcodes[z])<int(rows[middle][0]):
				right = middle
				middle = int((left+right)/2)
			else:
				left = middle
				middle =int((left+right)/2)
	#since the api code is private I have a filler var for it to remind me of its place
	#PUT IN API CODE TO TEST AND RUN
	res=""
	for c in coord:
		apiCodeFiller = ""
		units = ["imperial","metric","standard"]
		#INSERT API CODE FROM OPEN WEATHER API AFTER SIGNING UP AND WAITING A FEW HOURS (IF YOU HAVE A NEW ACCOUNT) AND THEN RUN
		response = requests.get("https://api.openweathermap.org/data/2.5/onecall?lat=" + c[0] + "&lon=" + c[1] + "&units="+units[unitsInd]+"&exclude=minutely,daily&appid="+""+apiCodeFiller)
		data = response.json()
		sunrise = time.strftime("%H:%M", time.localtime(int(data["current"]["sunrise"])))
		sunset = time.strftime("%H:%M", time.localtime(int(data["current"]["sunset"])))
		currentTemp = int(data["current"]["temp"])
		currentFeel = int(data["current"]["feels_like"])
		currentUVI = data["current"]["uvi"]
		currentDesc = data["current"]["weather"][0]["description"]
		currentWindSp = data["current"]["wind_speed"]
		#formats string evenly
		res += "Weather for zipcode " + zipcodes[coord.index(c)] +": \n\nSunrise & Sunset:\nSunrise: " + sunrise + "\nSunset: " +sunset + "\n\n"+"Current conditions: \nCurrent Temperature: " + str(currentTemp) + " degrees Fahrenheit" + "\nFeels like: " +str(currentFeel) +" degrees Fahrenheit\nCurrent condition: " + currentDesc + "\nUV index: " + str(currentUVI) + "\nWind Speed: " + str(currentWindSp) + " mph" + "\n\n" 
		#program starts running at  8:00 am and gives the current forecast for the day
		#finds temperature, feels like temp, percent chance of percipitation, condition, uvi index, and wind speed for each hour
		if unitsInd==0:
			tempArr = [str(int(data["hourly"][i]["temp"])) + " degrees Fahrenheit" for i in range(14)]
			feelArr=[str(int(data["hourly"][i]["feels_like"])) + " degrees Fahrenheit" for i in range(14)]
		elif unitsInd==1:
			tempArr = [str(int(data["hourly"][i]["temp"])) + " degrees Celsius" for i in range(14)]
			feelArr=[str(int(data["hourly"][i]["feels_like"])) + " degrees Celsius" for i in range(14)]
		else:
			tempArr = [str(int(data["hourly"][i]["temp"])) + " degrees Kelvin" for i in range(14)]
			feelArr=[str(int(data["hourly"][i]["feels_like"])) + " degrees Kelvin" for i in range(14)]
		percPrecArr = [str(100*data["hourly"][i]["pop"]) + "%" for i in range(14)]
		condArr=[data["hourly"][i]["weather"][0]["description"] for i in range(14)]
		uviArr=[data["hourly"][i]["uvi"] for i in range(14)]
		if unitsInd==0:
			windSpArr = [str(data["hourly"][i]["wind_speed"]) + " mph" for i in range(14)]
		else:
			windSpArr = [str(data["hourly"][i]["wind_speed"]) + " km/h" for i in range(14)]
		
		for i in range(14):
			res += time.strftime("%H:%M", time.localtime(int(data["hourly"][i]["dt"]))) + '\n'
			res+="Temperature: " + tempArr[i] + "\nFeels like: " + feelArr[i] + "\n"
			res+="Weather: " + condArr[i] + "\nChance of precipitation: " + percPrecArr[i] + "\n"
			res+="UV index: " + str(uviArr[i]) + "\nWind speed: " + windSpArr[i] + "\n\n"
		res += "\n\n\n"
	return res

#print(getHourlyForecast(0,["18976","19122"]))

if __name__ == '__main__':
	pass
