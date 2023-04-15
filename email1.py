import content
import yagmail
from datetime import date
import keys_and_passwords
#DO NOT LEAVE YOUR USER AND PASSWORD INFO HERE

class email1:
    def __init__(self):
        self.recipients = dict()
        #ENTER CORRESPONDING INFO FOR EMAIL YOU PLAN TO SET UP TO SEND INFO
        self.senderInfo = {'email':"",'password':keys_and_passwords.password}
        self.rList = [recipient for recipient in self.recipients]

    def changeRecipients(self,r):
        self.recipients=r
        return self.recipients

    def sendEmail(self):
        yag = yagmail.SMTP(self.senderInfo['email'],self.senderInfo['password'])
        for recipient in self.recipients:
            yag.send(to=recipient,subject="Weather and/or NBA Report for " + str(date.today()) + ":\n\n",contents = self.format(recipient))

    #individual formatting
    def format(self,recipient):
        text = ""
        if self.recipients[recipient][0][0] and content.getScores(self.recipients[recipient][1]):
            text+=content.getScores(self.recipients[recipient][1])
        if self.recipients[recipient][0][1] and content.getSchedule(self.recipients[recipient][1]):
            text+=content.getSchedule(self.recipients[recipient][1])
        if self.recipients[recipient][0][2] and content.getHourlyForecast(self.recipients[recipient][2][0],self.recipients[recipient][2][1]):
            text+=content.getHourlyForecast(self.recipients[recipient][2][0],self.recipients[recipient][2][1])
        return text


if __name__== '__main__':
    pass
