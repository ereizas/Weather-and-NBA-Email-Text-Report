import content
import yagmail
from datetime import date
#DO NOT LEAVE YOUR USER AND PASSWORD INFO HERE


class email1:
    def __init__(self):
        #score and schedule set to false for faster run time while testing format()
        self.content = {'score' : {'include':True,'content':content.getScores()},
        'schedule':{'include':True,'content':content.getSchedule()},
        'weather':{'include':True,'content':content.getHourlyForecast()}}

        self.recipients = ['']
        
        self.senderInfo = {'email':"",'password':''}
        pass

    def sendEmail(self):
        yag = yagmail.SMTP(self.senderInfo['email'],password = self.senderInfo['password'])
        for recipient in self.recipients:
            #change contents later
            yag.send(to=recipient,subject="Weather and/or NBA Report for " + str(date.today()) + ":\n\n",contents = email1().format())

    """sslPort = 465
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", sslPort, context=context) as server:
            server.login("", self.senderInfo["password"])
            for recipient in self.recipients:
                server.sendmail("", recipient, email1().format(),Subject="Weather and/or NBA Report for " + str(date.today()) + ":\n\n")"""

        


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
    em = email1()
    #with open('WANR Plain Text Test','w',encoding = 'utf-8') as f:
       #f.write(em.format())
    em.sendEmail()
