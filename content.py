#remove unused imports when finished
#get user input for teams and zipcode
from datetime import date, timedelta
#from requests.api import get
import re
from requests.api import get
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
import requests
import csv
import json
from urllib.request import urlopen



#the 200 means I am allowed to use the information
print(requests.get("https://www.espn.com/nba/scoreboard/_/date/"))




#NBA teams for which the user desires score and schedule updates
#array is added to via gui, text or email
#sample teams used to test algorithm, clear this later
teams = ["76ers","Bulls","Trail Blazers","Raptors","Bucks","Nets","Suns"]

#function within the primary functions getScores() and getSchedule()
def getTeamsPlay(soup,score):
    #finds the html code for the names of teams played and their scores in separate arrays
    playedList = soup.findAll("span",class_="sb-team-short")
    #converts all teams to string format in an array
    pList = [str(i)[str(i).index(">")+1:str(i).rfind("<")] for i in playedList]
    if score:
        timeList = soup.find_all(lambda x:
        (x.name == 'span' or x.name=="th") and
        ('time' in x.get('class', []) or 'date-time' in x.get('class', [])) and
        not 'cscore_time' in x['class'] and not 'date_time' in x.get('data-behavior',[]))

        #formats to array of times in string format
        tList =[str(i)[str(i).index(">")+1:str(i).rfind("<")].upper() for i in timeList]
        pListFinal = []
        for a in range(1,len(pList),2):
            if (pList[a-1] in teams or pList[a] in teams) and tList[int(a/2)]!="POSTPONED":
                pListFinal.append(pList[a-1])
                pListFinal.append(pList[a])
    
    else:
        #picks user's teams that played and the opposing team that day
        pListFinal = []
        for a in range(1,len(pList),2):
            if pList[a-1] in teams or pList[a] in teams:
                pListFinal.append(pList[a-1])
                pListFinal.append(pList[a])
    #creates an array with two arrays, with one for all teams playing/played and the other for just the ones of interest
    arr=[]
    arr.append(pList)
    arr.append(pListFinal)
    return arr

#check for what happens with postponed games
def getScores():
    #formats date for the link
    yesterday = str(date.today()-timedelta(days = 1)).replace("-","")

    #makes the default Google Chrome
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    #data I want is in <div id="events" class>
    driver.get("https://www.espn.com/nba/scoreboard/_/date/"+yesterday)
    content = driver.page_source
    soup = BeautifulSoup(content,features="html.parser")
    #html code array for score data
    scoreList = soup.findAll("td",class_="total")
    #builds str array of scores
    sList = []
    for i in scoreList:
        tempStr = ""
        #find("n") skips to later index that is before desired data for faster runtime
        for j in range(len(str(i)[str(i).find("n")]),len(str(i))):
            if(str(i)[j].isnumeric()):
                tempStr+=str(i)[j]
        sList.append(tempStr)
    
    #gets the desired information in same length arrays that match by index
    pListFinalRef = getTeamsPlay(soup,True)
    pListFinal = pListFinalRef[1]
    print(sList)
    sListFinal = [sList[pListFinalRef[0].index(b)] for b in pListFinal]
    
    res = "Yesterday's Scores: \n"
    for c in range(1,len(pListFinal),2):
        if int(sListFinal[c-1])>int(sListFinal[c]):
            res += pListFinal[c-1].upper() + " " *(32 - len(pListFinal[c-1])) + pListFinal[c] + "\n" +sListFinal[c-1] + " "*(32 - len(sListFinal[c-1])) + sListFinal[c] +"\n\n"
        elif int(sListFinal[c-1])<int(sListFinal[c]):
            res += pListFinal[c-1] + " " *(32 - len(pListFinal[c-1])) + pListFinal[c].upper() + "\n" +sListFinal[c-1] + " "*(32 - len(sListFinal[c-1])) + sListFinal[c] +"\n\n"
        else:
            res += pListFinal[c-1] + " " *(32 - len(pListFinal[c-1])) + pListFinal[c] + " POSTPONED\n"
    res+="*If you see that a game that you expected is not shown, then that game has been postponed.\n"
    return res


def getSchedule():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    #automatically goes to today's slate of NBA games
    driver.get("https://www.espn.com/nba/scoreboard/_/date/")
    content = driver.page_source
    soup = BeautifulSoup(content,features="html.parser")
    
    #the lambda function strictly matches those with class ="time" and if games are postponed it does the same but for the corresponding header
    #credit to Nuno Andre on https://stackoverflow.com/questions/14496860/how-to-beautiful-soup-bs4-match-just-one-and-only-one-css-class#14516768 for the lambda function
    timeList = soup.find_all(lambda x:
    (x.name == 'span' or x.name=="th") and
    ('time' in x.get('class', []) or 'date-time' in x.get('class', [])) and
    not 'cscore_time' in x['class'] and not 'date_time' in x.get('data-behavior',[]))

    #formats to array of times in string format
    tList =[str(i)[str(i).index(">")+1:str(i).rfind("<")].upper() for i in timeList]

    #same procedure as when done in getScores() function
    pListFinalRef = getTeamsPlay(soup,False)
    pListFinal = pListFinalRef[1]


    tListFinal = []
    #accounts for the fact that the number teams playing are double the amount of game times for the day
    for a in range(1,len(pListFinalRef[0]),2):
        if pListFinalRef[0][a-1] in teams or pListFinalRef[0][a] in teams:
            tListFinal.append(tList[int(a/2)])
    

    res = "Today's Slate: \n"
    for b in range(1,len(pListFinal),2):
        res+= pListFinal[b-1] + " at " + pListFinal[b] + " " + tListFinal[int(b/2)] + "\n\n"
    return res


def getHourlyForecast():
    #csv file from Eric Hurst at https://gist.github.com/erichurst/7882666
    file = open("ZIP,LAT,LNG.csv")
    csvreader = csv.reader(file)
    rows = []
    for line in csvreader:
        rows.append(line)
    #removes the first line
    rows = rows[1:]
    file.close()
    #to be replaced by user's zipcode
    zipcode = "18976"
    left = 0
    middle = int(len(rows)/2)
    right = len(rows)
    #lat,long
    coord = []
    #checks if csv file is sorted according to zip code and it checks out
    """for r in range(1,len(rows)):
        if int(rows[r][0])<int(rows[r-1][0]):
            print("f")"""
        
    while(len(coord)==0):
        if int(zipcode)==int(rows[middle][0]):
            coord.append(rows[middle][1].strip())
            coord.append(rows[middle][2].strip())
            break
        elif left==right:
            coord.append(rows[middle][1].strip())
            coord.append(rows[middle][2].strip())
        elif int(zipcode)<int(rows[middle][0]):
            right = middle
            middle = int((left+right)/2)
        else:
            left = middle
            middle =int((left+right)/2)
    print(coord)

    #read as an online json file
    response = requests.get("https://api.openweathermap.org/data/2.5/onecall?lat=" + coord[0] + "&lon=" + coord[1] + "&exclude=minutely,daily&appid=f36fe5c31fafd890a879027e3788a9bb")
    data = response.json()
    

getHourlyForecast()

if __name__ == '__main__':
    pass