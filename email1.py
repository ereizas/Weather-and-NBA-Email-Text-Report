import content
import yagmail
from datetime import date
#DO NOT LEAVE YOUR USER AND PASSWORD INFO HERE
#ENTER AN EMAIL FOR RECIPIENT TESTING

class email1:
    
    #figure out how to send individualized emails for teams and zipcodes
    def __init__(self):
        #format of user data
        self.recipients = dict()
        #self.recipients = []
        #ENTER CORRESPONDING INFO FOR EMAIL YOU PLAN TO SET UP TO SEND INFO
        self.senderInfo = {'email':"",'password':''}
        self.rList = [recipient for recipient in self.recipients]

    def changeRecipients(self,r):
        self.recipients=r
        return self.recipients

    def sendEmail(self):
        yag = yagmail.SMTP(self.senderInfo['email'],password = self.senderInfo['password'])
        for recipient in self.recipients:
            yag.send(to=recipient,subject="Weather and/or NBA Report for " + str(date.today()) + ":\n\n",contents = self.format(recipient))

    #individual formatting
    def format(self,recipient):
        text = ""
        if self.recipients[recipient][0][0] and content.getScores(self.recipients[recipient][1]):
            text+=content.getScores(self.recipients[recipient][1])
        if self.recipients[recipient][0][1] and content.getSchedule(self.recipients[recipient][1]):
            text+=content.getSchedule(self.recipients[recipient][1])
        if self.recipients[recipient][0][2] and content.getHourlyForecast(self.recipients[recipient][2]):
            text+=content.getHourlyForecast(self.recipients[recipient][2])
        return text


if __name__== '__main__':
    pass
