from datetime import date, timedelta
from requests.api import get

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
teams = ["Sixers","Bulls","Heat","Warriors","Trail Blazers","Raptors"]

def getScores():
    #formats date for the link
    yesterday = str(date.today()-timedelta(days = 1)).replace("-","")


    #makes the default Google Chrome
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    #data I want is in <div id="events" class>
    driver.get("https://www.espn.com/nba/scoreboard/_/date/"+yesterday)
    content = driver.page_source
    soup = BeautifulSoup(content,features="html.parser")
    
    #finds the html code for the names of teams played and their scores in separate arrays
    playedList = soup.findAll("span",class_="sb-team-short")
    scoreList = soup.findAll("td",class_="total")
    #builds string list of teams and str array of scores
    pList = [str(i)[str(i).index(">")+1:str(i).rfind("<")] for i in playedList]
    
    sList = []
    for i in scoreList:
        tempStr = ""
        for j in str(i):
            if(j.isnumeric()):
                tempStr+=j
        sList.append(tempStr)
    
    #gets the desired information in same length arrays that match by index
    pListFinal = []
    for a in range(1,len(pList),2):
        if pList[a-1] in teams or pList[a] in teams:
            pListFinal.append(pList[a-1])
            pListFinal.append(pList[a])
    sListFinal = [sList[pList.index(b)] for b in pListFinal]
    print(pListFinal)
    print(sListFinal)
    
    res = ""
    for c in range(1,len(pListFinal),2):
        if sListFinal[c-1]>sListFinal[c]:
            res += pListFinal[c-1].upper() + " " *(32 - len(pListFinal[c-1])) + pListFinal[c] + "\n" +sListFinal[c-1] + " "*(32 - len(sListFinal[c-1])) + sListFinal[c] +"\n\n"
        else:
            res += pListFinal[c-1] + " " *(32 - len(pListFinal[c-1])) + pListFinal[c].upper() + "\n" +sListFinal[c-1] + " "*(32 - len(sListFinal[c-1])) + sListFinal[c] +"\n\n"
    return res


def getSchedule():
    today = str(date.today().replace("-",""))


    pass

def getHourlyForecast():
    pass

if __name__ == '__main__':
    pass