from tkinter import *
from tkinter import ttk
from email1 import email1
from scheduler import emailScheduler
#needs to help choose content, add/remove recipients, keep track of user's preferred zipcode(s), team(s) and information, schedule for 8 am EST, and configure sender credentials
#check boxes for preferred content -> 
#list of emails -> remove selected w a button, add with a text box and "add" button
class emailGUI():
    def __init__(self,root):
        #header/title
        self.__root = root
        self.__root.title('NBA and/or Weather Report')
        title_label = ttk.Label(self.__root, text = "NBA and/or Weather Report", font = 'Daytona 35 bold', justify=CENTER)
        #size
        title_label.pack(padx=5,pady=5)
        
        self.__style = ttk.Style()
        self.__style.configure('TButton',font = ('Daytona',12,'bold'))
        self.__style.configure('Header.TLabel',font = ('Daytona',18,'bold'))

        #GUI list for recipients
        #later try to make open to users to input email and other info
        recipientsFrame = ttk.Frame(self.__root)
        recipientsFrame.pack(padx=5,pady=5)
        self.addRecipientVar = StringVar()
        self.recipList = Variable()
        self.buildGuiRecipients(recipientsFrame,self.addRecipientVar,self.recipList)
        #gui to schedule delivery time, set to 8 am
        scheduleFrame = ttk.Frame(self.__root)
        scheduleFrame.pack(padx=5,pady=5)

        #self.hourVar = StringVar()#.set('08')
        #self.minuteVar = StringVar()#.set('00')
        #self.buildGuiSchedule(scheduleFrame,self.hourVar,self.minuteVar)

        #gui checkboxes of content
        contentsFrame = ttk.Frame(self.__root)
        contentsFrame.pack(padx=5,pady=5)
        #boolean for check or unchecked
        self.scoreVar = BooleanVar()
        self.scheduleVar = BooleanVar()
        self.weatherVar = BooleanVar()
        self.buildGuiContents(contentsFrame,self.scoreVar,self.scheduleVar,self.weatherVar)
        #GUI for sender credentials
        senderFrame = ttk.Frame(self.__root)
        senderFrame.pack(padx=5,pady=5)
        self.senderEmailVar = StringVar()
        self.senderPasswordVar = StringVar()
        self.buildGuiSender(senderFrame,self.senderEmailVar,self.senderPasswordVar)
        #GUI for controls
        controlsFrame = ttk.Frame(self.__root)
        controlsFrame.pack(padx=5,pady=5)
        self.buildGuiControls(controlsFrame)

        #intialize vars
        #maybe add args to email1 according to the booleanVars
        self.__email = email1()

        self.addRecipientVar.set('')
        self.recipList.set(self.__email.recipient)

        #self.hourVar.set('08')
        #self.minuteVar.set('00')

        self.scoreVar.set(self.__email.content['score']['include'])
        self.scheduleVar.set(self.__email.content['schedule']['include'])
        self.weatherVar.set(self.__email.content['weather']['include'])

        self.senderEmailVar.set(self.__email.senderInfo['email'])
        self.senderPasswordVar.set(self.__email.senderInfo['password'])

        #initialize scheduler 
        self.scheduler = emailScheduler()
        self.scheduler.start()
        self.__root.protocol("WM_DELETE_WINDOW",self.__shutdown)


    
    def buildGuiRecipients(self,master,addRecipientVar,recipList):
        #widgets
        header = ttk.Label(master,text = 'Recipients: ', style = "Header.TLabel")
        spacer_frame = ttk.Frame(master) #for spacing

        recipientsEntry = ttk.Entry(master,width=40, textvariable=addRecipientVar)
        recipientsScrollbar = ttk.Scrollbar(master,orient=VERTICAL)
        recipientsScrollbar.grid(row = 4, column =1, sticky = N+S+W+E)
        recipientsListbox = Listbox(master, listvariable=recipList, selectmode='multiple', width=40,height =5)
        recipientsListbox.configure(yscrollcommand=recipientsScrollbar.set())
        recipientsScrollbar.config(command=recipientsListbox.yview)
        #possibly make a fxn for add recipient
        addButton = ttk.Button(master, text='Add Recipient', command = self.addRecipient)
        removeButton = ttk.Button(master,text='Remove Selected',command = lambda: self.removeRecipients(recipList))

        #placement of widgets
        header.grid(row=0,column=0)
        recipientsEntry.grid(row=1,column=0)
        addButton.grid(row=2,column=0)
        #pady extends vertical boundry
        spacer_frame.grid(row=3,column=0,pady=5)
        recipientsListbox.grid(row=4,colum=0)
        removeButton.grid(row=5,column=0)

    #might not want a gui for schedule since I want it constant at 8 am
    def buildGuiSchedule(self, master, hourVar,minuteVar):
        pass

    def buildGuiContents(self, master, scoreVar, scheduleVar, weatherVar):
        
        pass

    def buildGuiSender(self, master, senderEmailVar,senderPasswordVar):
        pass

    def buildGuiControls():
        pass

    def addRecipient():
        pass

    def removeRecipients():
        pass

if __name__== "__main__":
    root = Tk()
    app = emailGUI(root)
    root.mainloop()