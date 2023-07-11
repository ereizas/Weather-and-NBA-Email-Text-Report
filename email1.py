import content
import yagmail
from datetime import date
import keys_and_passwords
#DO NOT LEAVE YOUR USER AND PASSWORD INFO HERE

class email1:
    def __init__(self):
        self.recipients = dict()
        self.senderInfo = {'email':keys_and_passwords.emailAddr,'password':keys_and_passwords.password}
        self.rList = [recipient for recipient in self.recipients]

    def changeRecipients(self,r):
        """
        Changes the dictionary self.recipients
        @param r : value to reassign self.recipients to
        @return self.recipients : new value of self.recipients
        """

        self.recipients=r
        return self.recipients

    def sendEmail(self):
        """
        Logs in to email and sends an email with requested info to each recipient
        """

        yag = yagmail.SMTP(self.senderInfo['email'],self.senderInfo['password'])
        allTeamsPlayed, allScores = [], []
        #if any of the recipients wants NBA scores from yesterday
        if any(self.recipients[recip][0][0] for recip in self.recipients):
            allTeamsPlayed, allScores = content.getAllNBAScores()

        allTeamsPlaying, allTimes = [], []
        if any(self.recipients[recip][0][1] for recip in self.recipients):
            allTeamsPlaying, allTimes = content.getAllNBASchedules()

        coordRows=[]
        if any(self.recipients[recip][0][2] for recip in self.recipients):
            coordRows = content.getCoordRows()

        for recipient in self.recipients:
            yag.send(to=recipient,subject="Weather and/or NBA Report for " + str(date.today()) + ":\n\n",contents = self.format(recipient,allTeamsPlayed,allScores,allTeamsPlaying,allTimes,coordRows))
        

    #individual formatting
    def format(self,recipient,allTeamsPlayed,allScores,allTeamsPlaying,allTimes,coordRows):
        """
        Adds information that the user requested to the contents of the email
        @param recpient : email address for a user
        @param allTeamsPlayed : list of all NBA teams that played yesterday
        @param allScores : list of all NBA scores from yesterday
        @param allTeamsPlaying : list of all NBA teams scheduled to play a game today
        @param allTimes : list of all times that NBA teams are scheduled to play a game today
        @param coordRows : rows from the zipcode coordinate csv file
        """

        text = ""
        if self.recipients[recipient][0][0]:
            text+=content.getScores(self.recipients[recipient][1],allTeamsPlayed,allScores)
        if self.recipients[recipient][0][1]:
            text+=content.getSchedule(self.recipients[recipient][1],allTeamsPlaying,allTimes)
        if self.recipients[recipient][0][2]:
            text+=content.getHourlyForecast(self.recipients[recipient][2][0],self.recipients[recipient][2][1],coordRows)
        return text


if __name__== '__main__':
    pass
