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
        if any(recip[1] for recip in self.recipients):
            allTeamsPlayed, allScores = content.getAllTeamsAndScores()
        for recipient in self.recipients:
            yag.send(to=recipient,subject="Weather and/or NBA Report for " + str(date.today()) + ":\n\n",contents = self.format(recipient,allTeamsPlayed,allScores))

    #individual formatting
    def format(self,recipient,allTeamsPlayed, allScores):
        """
        Adds information that the user requested to the contents of the email
        @param recpient : email address for a user
        @param allTeamsPlayed : list of all NBA teams that played yesterday
        @param allScores : list of all NBA scores from yesterday
        """

        text = ""
        if self.recipients[recipient][0][0]:
            text+=content.getScores(self.recipients[recipient][1],allTeamsPlayed,allScores)
        if self.recipients[recipient][0][1]:
            text+=content.getSchedule(self.recipients[recipient][1])
        if self.recipients[recipient][0][2]:
            text+=content.getHourlyForecast(self.recipients[recipient][2][0],self.recipients[recipient][2][1])
        return text


if __name__== '__main__':
    pass
