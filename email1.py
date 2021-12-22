import content
from datetime import date
class email1:
    def __init__(self):
        #score and schedule set to false for faster run time while testing format()
        self.content = {'score' : {'include':True,'content':content.getScores()},
        'schedule':{'include':True,'content':content.getSchedule()},
        'weather':{'include':True,'content':content.getHourlyForecast()}}
        pass

    def sendEmail(self):
        pass

    def format(self):
        text = "Weather and/or NBA Report for " + str(date.today()) + ":\n\n"
        if self.content['score']['include'] and self.content['score']['content']:
            text+=self.content['score']['content']
        if self.content['schedule']['include'] and self.content['schedule']['content']:
            text+=self.content['schedule']['content']
        if self.content['weather']['include'] and self.content['weather']['content']:
            text+=self.content['weather']['content']
        return text


if __name__== '__main__':
    em = email1()
    with open('WANR Plain Text Test','w',encoding = 'utf-8') as f:
        f.write(em.format())
