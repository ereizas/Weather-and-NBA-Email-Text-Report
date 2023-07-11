import time
import requests
import content_jsons
import keys_and_passwords
from datetime import date, timedelta
import csv
def getAllTeamsAndScores():
	"""
	Retrieves all the teams that played yesterday and the respective scores
	@return teamsPlayed : list of all the teams that played yesterday
	@return scores : llist of scores for the teams that played yesterday
	"""

	yesterday = str(date.today()-timedelta(days = 1))
	url = "https://www.balldontlie.io/api/v1/games?start_date=" +yesterday + "&end_date=" + yesterday
	response = requests.get(url)
	scoresJSON = response.json()
	#index for teamsPlayed and scores
	i = 0
	#initialized this way so that the first conditional in the for loop will not throw an error
	teamsPlayed = [[]]
	scores = [[]]
	if scoresJSON['data']!=[]:
		#goes through all elememts since the two team are in separate dictionaries in the larger dictionary for each game
		for a in range(len(scoresJSON["data"])):
			if teamsPlayed[i]!=[] and scores[i]!=[]:
				i+=1
				#creates the arrays that the following for loop will add to
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
		return [],[]
	return teamsPlayed, scores

def getScores(teams:list[str],allTeamsPlayed:list[str],allScores:list[str])->str:
	"""
	Returns a string with scores from yesterday for certain teams
	@param teams : list of str names of teams
	@param allTeamsPlayed : list of all the NBA teams that played yesterday
	@param allScores : list of scores for teams that played yesterday
	@return : str informing user of scores of teams they prefer from yesterday or a message saying otherwise
	"""
	scores = []
	teamsPlayed = []
	if(len(allTeamsPlayed)!=0):
		res = "Yesterday's Scores: \n"
		for t in range(len(allTeamsPlayed)):
			if(allTeamsPlayed[t][0] in teams or allTeamsPlayed[t][1] in teams):
				#appends array pair of the two teams that faced off and another two element array of the respective scores
				teamsPlayed.append(allTeamsPlayed[t])
				scores.append(allScores[t])
		for t in range(len(teamsPlayed)):
			if scores[t][0]>scores[t][1]:
				res += teamsPlayed[t][0] + " beat " + teamsPlayed[t][1] + " " + str(scores[t][0]) + "-" + str(scores[t][1]) + "\n\n"
			elif scores[t]>scores[t]:
				res += teamsPlayed[t][1] + " beat " + teamsPlayed[t][0] + " " + str(scores[t][1]) + "-" + str(scores[t][0]) + "\n\n"
		##check what to do w these
		if res =="Yesterday's Scores: \n":
			return "*Your teams did not play any games yesterday.\n\n\n\n\n"
		res+="*If a game that you expected is not shown, then that game may have been postponed.\n\n\n\n\n"
		return res
	else:
		return "*No NBA games were played yesterday.\n\n\n\n\n"
	

#print(getScores(["76ers","Bulls","Trail Blazers","Raptors","Bucks","Nets","Suns"]))

def getSchedule(teams:list[str])->str:
	"""
	Returns a string with the schedule for today for teams in teams
	@param teams : list of str team names
	@return : str informing user of the schedule for today for teams they prefer or a message saying otherwise
	"""
	teamsPlaying = []
	playTimes = []
	if len(content_jsons.teamsPlaying)>0:
		res = "Today's Slate: \n"
		for t in range(len(content_jsons.teamsPlaying)):
			if(content_jsons.teamsPlaying[t][0] in teams or content_jsons.teamsPlaying[t][1] in teams):
				teamsPlaying.append(content_jsons.teamsPlaying[t])
				playTimes.append(content_jsons.playTimes[t])
		for s in range(len(teamsPlaying)):
			res+= teamsPlaying[s][1] + " at " + teamsPlaying[s][0] + " " + playTimes[int(s/2)] + "\n\n"
		if res == "Today's Slate: \n":
			return "*Your teams are not playing any games today.\n\n\n\n\n"
		return res + "\n\n\n\n\n"				
	else:
		return "*There are no NBA Games scheduled for today.\n\n\n\n\n"

#print(getSchedule(["76ers","Bulls","Trail Blazers","Raptors","Bucks","Nets","Suns"]))

def getCoords(zipcodes:list[str])->list[list[str]]:
	"""
	Retrieves coordinate pairs for specified zipcodes
	@param zipcodes : list of str zipcodes that the user wants the forecast for
	@return coords : list of coordinate pairs for each zipcode
	"""

	#removes invalid zipcodes
	zipcodes = [zipcode for zipcode in zipcodes if zipcode in [i[0] for i in content_jsons.rows]]
	coords = [[] for i in zipcodes]
	#extract coordinates for each zipcode in zipcodes array via binary search
	for z in range(len(zipcodes)):
		left = 0
		middle = int(len(content_jsons.rows)/2)
		right = len(content_jsons.rows)
		while(coords[z]==[]):
			if int(zipcodes[z])==int(content_jsons.rows[middle][0]):
				coords[z].append(content_jsons.rows[middle][1].strip())
				coords[z].append(content_jsons.rows[middle][2].strip())
				break
			elif left==right:
				coords[z].append(content_jsons.rows[middle][1].strip())
				coords[z].append(content_jsons.rows[middle][2].strip())
				break
			elif int(zipcodes[z])<int(content_jsons.rows[middle][0]):
				right = middle
				middle = int((left+right)/2)
			else:
				left = middle
				middle =int((left+right)/2)
	return coords

def getHourlyForecast(unitsInd:int,zipcodes:list[str])->str:
	"""
	Returns a string with hourly forecast information for preferred zipcodes
	@param unitsInd : index into units array to determine which unit of temperature out of Fahrenheit, Celsius, and Kelvin the user wants
	@param zipcodes : list of str zipcodes the user wants the weather for
	"""
	
	res=""
	coords = getCoords(zipcodes)
	for c in coords:
		apiKey = keys_and_passwords.apiKey
		units = ["imperial","metric","standard"]
		response = requests.get("https://api.openweathermap.org/data/2.5/onecall?lat=" + c[0] + "&lon=" + c[1] + "&units="+units[unitsInd]+"&exclude=minutely,daily&appid="+apiKey)
		data = response.json()
		sunrise = time.strftime("%H:%M", time.localtime(int(data["current"]["sunrise"])))
		sunset = time.strftime("%H:%M", time.localtime(int(data["current"]["sunset"])))
		currentTemp = int(data["current"]["temp"])
		currentFeel = int(data["current"]["feels_like"])
		currentUVI = data["current"]["uvi"]
		currentDesc = data["current"]["weather"][0]["description"]
		currentWindSp = data["current"]["wind_speed"]
		#formats string evenly
		res += "Weather for zipcode " + zipcodes[coords.index(c)] +": \n\nSunrise & Sunset:\nSunrise: " + sunrise + "\nSunset: " +sunset + "\n\n"+"Current conditions: \nCurrent Temperature: " + str(currentTemp) + " degrees Fahrenheit" + "\nFeels like: " +str(currentFeel) +" degrees Fahrenheit\nCurrent condition: " + currentDesc + "\nUV index: " + str(currentUVI) + "\nWind Speed: " + str(currentWindSp) + " mph" + "\n\n" 
		#finds temperature, feels like temp, percent chance of percipitation, condition, uvi index, and wind speed for each hour
		hours = 14
		if unitsInd==0:
			tempArr = [str(int(data["hourly"][i]["temp"])) + " degrees Fahrenheit" for i in range(hours)]
			feelArr=[str(int(data["hourly"][i]["feels_like"])) + " degrees Fahrenheit" for i in range(hours)]
		elif unitsInd==1:
			tempArr = [str(int(data["hourly"][i]["temp"])) + " degrees Celsius" for i in range(hours)]
			feelArr=[str(int(data["hourly"][i]["feels_like"])) + " degrees Celsius" for i in range(hours)]
		else:
			tempArr = [str(int(data["hourly"][i]["temp"])) + " degrees Kelvin" for i in range(hours)]
			feelArr=[str(int(data["hourly"][i]["feels_like"])) + " degrees Kelvin" for i in range(hours)]
		percPrecArr = [str(100*data["hourly"][i]["pop"]) + "%" for i in range(hours)]
		condArr=[data["hourly"][i]["weather"][0]["description"] for i in range(hours)]
		uviArr=[data["hourly"][i]["uvi"] for i in range(hours)]
		if unitsInd==0:
			windSpArr = [str(data["hourly"][i]["wind_speed"]) + " mph" for i in range(hours)]
		else:
			windSpArr = [str(data["hourly"][i]["wind_speed"]) + " km/h" for i in range(hours)]
		for i in range(hours):
			res += time.strftime("%H:%M", time.localtime(int(data["hourly"][i]["dt"]))) + '\n'
			res+="Temperature: " + tempArr[i] + "\nFeels like: " + feelArr[i] + "\n"
			res+="Weather: " + condArr[i] + "\nChance of precipitation: " + percPrecArr[i] + "\n"
			res+="UV index: " + str(uviArr[i]) + "\nWind speed: " + windSpArr[i] + "\n\n"
		res += "\n\n\n"
	return res

#print(getHourlyForecast(0,["18976","19122"]))

if __name__ == '__main__':
	pass
