import time, csv
import content_jsons

def getScores(teams):
	scores = []
	teamsPlayed = []
	if(len(content_jsons.teamsPlayed)!=0):
		res = "Yesterday's Scores: \n"
		for t in range(len(content_jsons.teamsPlayed)):
			if(content_jsons.teamsPlayed[t][0] in teams or content_jsons.teamsPlayed[t][1] in teams):
				teamsPlayed.append(content_jsons.teamsPlayed[t])
				scores.append(content_jsons.scores[t])
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

def getSchedule(teams):
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

print(getSchedule(["76ers","Bulls","Trail Blazers","Raptors","Bucks","Nets","Suns"]))

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
	for z in range(len(zipcodes)):
		left = 0
		middle = int(len(rows)/2)
		right = len(rows)
		while(coord[z]==[]):
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
	res=""
	for c in coord:
		data = getForecastJSON(c,unitsInd)
		sunrise = time.strftime("%H:%M", time.localtime(int(data["current"]["sunrise"])))
		sunset = time.strftime("%H:%M", time.localtime(int(data["current"]["sunset"])))
		currentTemp = int(data["current"]["temp"])
		currentFeel = int(data["current"]["feels_like"])
		currentUVI = data["current"]["uvi"]
		currentDesc = data["current"]["weather"][0]["description"]
		currentWindSp = data["current"]["wind_speed"]
		#formats string evenly
		res += "Weather for zipcode " + zipcodes[coord.index(c)] +": \n\nSunrise & Sunset:\nSunrise: " + sunrise + "\nSunset: " +sunset + "\n\n"+"Current conditions: \nCurrent Temperature: " + str(currentTemp) + " degrees Fahrenheit" + "\nFeels like: " +str(currentFeel) +" degrees Fahrenheit\nCurrent condition: " + currentDesc + "\nUV index: " + str(currentUVI) + "\nWind Speed: " + str(currentWindSp) + " mph" + "\n\n" 
		#program starts running at 8:00 am and gives the current forecast for the day
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
