from datetime import date, timedelta
from requests.api import get
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
import requests
import urllib.request

url = "https://www.espn.com/nba/scoreboard/_/date/"
#the 200 means I am allowed to use the information
print(requests.get(url))

#NBA teams for which the user desires score and schedule updates
#added to via gui, text or email
#sample teams used to test algorithm, clear this later
teams = ["Sixers","Bulls","Trail Blazers","Raptors","Bucks","Nets","Suns"]

#function within the primary functions getScores() and getSchedule()
def getTeamsPlay(soup):
    #finds the html code for the names of teams played and their scores in separate arrays
    playedList = soup.findAll("span",class_="sb-team-short")
    #converts all teams to string format in an array
    pList = [str(i)[str(i).index(">")+1:str(i).rfind("<")] for i in playedList]
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
    print(scoreList)
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
    pListFinalRef = getTeamsPlay(soup)
    pListFinal = pListFinalRef[1]
    sListFinal = [sList[pListFinalRef[0].index(b)] for b in pListFinal]
    
    res = ""
    for c in range(1,len(pListFinal),2):
        if int(sListFinal[c-1])>int(sListFinal[c]):
            res += pListFinal[c-1].upper() + " " *(32 - len(pListFinal[c-1])) + pListFinal[c] + "\n" +sListFinal[c-1] + " "*(32 - len(sListFinal[c-1])) + sListFinal[c] +"\n\n"
        else:
            res += pListFinal[c-1] + " " *(32 - len(pListFinal[c-1])) + pListFinal[c].upper() + "\n" +sListFinal[c-1] + " "*(32 - len(sListFinal[c-1])) + sListFinal[c] +"\n\n"
    return res


def getSchedule():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    #automatically goes to today's slate of NBA games
    driver.get("https://www.espn.com/nba/scoreboard/_/date/")
    content = driver.page_source
    soup = BeautifulSoup(content,features="html.parser")
    #the lambda function strictly matches those with class ="time"
    #credit to Nuno Andre on https://stackoverflow.com/questions/14496860/how-to-beautiful-soup-bs4-match-just-one-and-only-one-css-class#14516768 for the lambda function
    timeList = soup.find_all(lambda x:
    x.name == 'span' and
    'time' in x.get('class', []) and
    not 'cscore_time' in x['class'])
    print(timeList)
    pListFinalRef = getTeamsPlay(soup)
    pListFinal = pListFinalRef[1]

getSchedule()


def getHourlyForecast():
    pass

if __name__ == '__main__':
    pass