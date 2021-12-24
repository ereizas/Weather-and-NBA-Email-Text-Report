import content
import yagmail
from datetime import date
#DO NOT LEAVE YOUR USER AND PASSWORD INFO HERE
#ENTER AN EMAIL FOR RECIPIENT TESTING

class email1:
    """def __init__(self):
        self.content = {'score' : {'include':True,'content':content.getScores()},
        'schedule':{'include':True,'content':content.getSchedule()},
        'weather':{'include':True,'content':content.getHourlyForecast()}}
        #enter an email
        self.recipient = ['']
        #enter email that was set up for this
        self.senderInfo = {'email':"",'password':'^'}"""
        

    def __init__(self,includeScore,includeSchedule,includeWeather,teams, zipcodes,recipient):
        self.content = {'score' : {'include':includeScore,'content':content.getScores(teams)},
        'schedule':{'include':includeSchedule,'content':content.getSchedule(teams)},
        'weather':{'include':includeWeather,'content':content.getHourlyForecast(zipcodes)}}
        self.recipient = '' #recipient
        self.senderInfo = {'email':"",'password':''}

    def sendEmail(self):
        yag = yagmail.SMTP(self.senderInfo['email'],password = self.senderInfo['password'])
        for recipient in self.recipients:
            #change contents later
            yag.send(to=recipient,subject="Weather and/or NBA Report for " + str(date.today()) + ":\n\n",contents = email1().format())

    def format(self):
        text = ""
        if self.content['score']['include'] and self.content['score']['content']:
            text+=self.content['score']['content']
        if self.content['schedule']['include'] and self.content['schedule']['content']:
            text+=self.content['schedule']['content']
        if self.content['weather']['include'] and self.content['weather']['content']:
            text+=self.content['weather']['content']
        return text


if __name__== '__main__':
    #em = email1(True,True,True,'')
    #with open('WANR Plain Text Test','w',encoding = 'utf-8') as f:
       #f.write(em.format())
    #em.sendEmail()
    pass
