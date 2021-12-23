import content
class text:
    def __init__(self):
        self.content = {'score' : {'include':True,'content':content.getScores()},
        'schedule':{'include':True,'content':content.getSchedule()},
        'weather':{'include':True,'content':content.getHourlyForecast()}}

        

    def sendText(self):
        pass

    def format(self):
        pass

    if __name__== '__main__':
        pass #test code?