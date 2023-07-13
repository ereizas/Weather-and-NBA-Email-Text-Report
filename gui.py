from tkinter import *
from tkinter import ttk
from email1 import email1
import json
import os
#gui allows choosing content, adding/removing of recipients, keeping track of user's preferred zipcode(s), team(s) and information, and configure sender credentials
class emailGUI():
	def __init__(self,root:Tk):
		#bool for whether program is running
		self.running = True
		#header/title
		self.__root = root
		self.__root.title('NBA and/or Weather Report')
		title_label = ttk.Label(self.__root, text = "NBA and/or Weather Report", font = 'Daytona 30 bold', justify=CENTER)
		#size
		title_label.pack(padx=5,pady=5)
		mainFrame = ttk.Frame(self.__root)
		mainFrame.pack(fill=BOTH,expand=1,anchor=CENTER)
		canv = Canvas(mainFrame)
		canv.pack(side=LEFT,fill=BOTH,expand=1,anchor=CENTER)
		mainScrollBar = ttk.Scrollbar(mainFrame,orient=VERTICAL,command=canv.yview)
		mainScrollBar.pack(side='right',fill=Y)
		canv.configure(yscrollcommand=mainScrollBar.set,)
		canv.bind('<Configure>', lambda e: canv.configure(scrollregion=canv.bbox("all")))
		secondFrame = Frame(canv)
		secondFrame.pack(fill=BOTH,expand=1)
		canv.create_window((secondFrame.winfo_screenwidth()/2, secondFrame.winfo_screenheight()/2), window=secondFrame, anchor="center",height=800,width=3000)
		
		self.__style = ttk.Style()
		self.__style.configure('TButton',font = ('Daytona',12,'bold'))
		self.__style.configure('Header.TLabel',font = ('Daytona',18,'bold'))

		self.__email = email1()
		#loads configuration
		with open('wanbarConfig.json') as file:
			self.__email.recipients = json.load(file)

		recipientsFrame = ttk.Frame(secondFrame)
		recipientsFrame.pack(padx=5,pady=5)
		self.recipList = Variable()
		self.rInd = 0
		self.recipList.set(self.__email.rList)

		#stores all the necessary information for each user
		self.buildGuiRecipients(recipientsFrame,self.recipList)

		#gui checkboxes of content
		contentsFrame = ttk.Frame(secondFrame)
		contentsFrame.pack(padx=5,pady=5)
		#boolean for check or unchecked
		self.scoreVar = BooleanVar()
		self.scheduleVar = BooleanVar()
		self.weatherVar = BooleanVar()
		self.unitVar = IntVar()
		self.teamList = Variable()
		self.tInd = 0

		self.zipcode=StringVar()#add to array below
		self.zipList = Variable()
		self.zInd = 0
		self.teamList.set([])
		self.zipcode.set('')
		self.zipList.set([])
		self.buildGuiContents(contentsFrame,self.scoreVar,self.scheduleVar,self.weatherVar,self.teamList,self.zipcode,self.zipList)
		#GUI for sender credentials
		senderFrame = ttk.Frame(secondFrame)
		senderFrame.pack(padx=5,pady=5)
		self.senderEmailVar = StringVar()
		self.senderPasswordVar = StringVar()
		self.senderEmailVar.set(self.__email.senderInfo['email'])
		self.senderPasswordVar.set(self.__email.senderInfo['password'])
		self.buildGuiSender(senderFrame,self.senderEmailVar,self.senderPasswordVar)
		#GUI for controls
		controlsFrame = ttk.Frame(secondFrame)
		controlsFrame.pack(padx=5,pady=5)
		self.buildGuiControls(controlsFrame)
	
	def buildGuiRecipients(self,master,recipList):
		#widgets
		header = ttk.Label(master,text = 'Recipient email: ', style = "Header.TLabel")
		spacer_frame = ttk.Frame(master) #for spacing

		self.recipientsEntry = ttk.Entry(master,width=40)
		recipientsScrollbar = ttk.Scrollbar(master,orient=VERTICAL)
		recipientsScrollbar.grid(row = 3, column =1, sticky = N+S+W+E)
		self.recipientsListbox = Listbox(master, listvariable=recipList, selectmode='multiple', width=40,height =5)
		self.recipientsListbox.configure(yscrollcommand=recipientsScrollbar.set)
		recipientsScrollbar.config(command=self.recipientsListbox.yview)
		removeButton = ttk.Button(master,text='Remove Selected',command = lambda: self.removeRecipients(self.recipientsListbox.curselection()))

		#placement of widgets
		header.grid(row=0,column=0)
		self.recipientsEntry.grid(row=1,column=0)
		#pady extends vertical boundry
		spacer_frame.grid(row=2,column=0,pady=5)
		self.recipientsListbox.grid(row=3,column=0)
		removeButton.grid(row=4,column=0)

	def buildGuiContents(self, master, scoreVar, scheduleVar, weatherVar,teams,zipcode,zipcodes):
		header = ttk.Label(master,text = 'Content Selection: ', style = "Header.TLabel")
		spacer_frame = ttk.Frame(master)
		spacerHorz = ttk.Frame(master)
		scoreCheckbox = ttk.Checkbutton(master,text="NBA Scores from Yesterday",variable=scoreVar)
		scheduleCheckbox = ttk.Checkbutton(master,text="NBA Schedule for Today", variable = scheduleVar)
		weatherCheckbox= ttk.Checkbutton(master,text="Hourly Weather Forecast",variable=weatherVar)

		#all team names to choose from and how to input them
		allTeams = ['76ers','Bucks','Bulls','Cavaliers','Celtics','Clippers','Grizzlies','Hawks','Heat','Hornets','Jazz','Kings','Knicks','Lakers',
		'Magic','Mavericks','Nets','Nuggets','Pacers','Pelicans','Pistons','Raptors','Rockets','Spurs','Suns','Thunder','Timberwolves','Trail Blazers','Warriors','Wizards']
		allTeamScrollbar = ttk.Scrollbar(master,orient=VERTICAL)
		#change row later depending on what you add
		allTeamScrollbar.grid(row = 1, column =3, sticky = N+S+W+E)
		allTeamListbox = Listbox(master, selectmode='multiple', width=40,height =5)
		for t in range(len(allTeams)):
			allTeamListbox.insert(t,allTeams[t])
		allTeamListbox.configure(yscrollcommand=allTeamScrollbar.set)
		allTeamScrollbar.config(command=allTeamListbox.yview())

		#entering/removing preferred teams
		teamEntryLabel = ttk.Label(master,text='Enter a team name as shown above')
		allTeamLabel = ttk.Label(master,text='All NBA Teams',style="Header.TLabel")
		self.teamEntry = ttk.Entry(master,width=40)
		teamScrollbar = ttk.Scrollbar(master,orient=VERTICAL)
		teamScrollbar.grid(row = 7, column =3, sticky = N+S+W+E)
		self.teamListbox = Listbox(master, listvariable=teams, selectmode='multiple', width=40,height =5)
		self.teamListbox.configure(yscrollcommand=teamScrollbar.set)
		teamScrollbar.config(command=self.teamListbox.yview())
		addTeamButton = ttk.Button(master, text='Add NBA Team', command = self.addTeam)
		removeTeamButton = ttk.Button(master,text='Remove Selected Teams',command = lambda: self.removeTeams(self.teamListbox.curselection()))
		prefNBATeamLabel = ttk.Label(master,text='Preferred NBA Teams',style = "Header.TLabel")

		#entering of preferred zipcodes
		unitEntryLabel = ttk.Label(master,text="Enter 0 for Imperial (US), 1 for Metric, or 2 for Standard:")
		unitEntry = ttk.Entry(master,width=5,textvariable=self.unitVar)
		zipEntryLabel = ttk.Label(master,text = "Enter a 5 digit zipcode:")
		self.zipcodeEntry = ttk.Entry(master,width=40,textvariable=zipcode)
		zipcodeScrollbar = ttk.Scrollbar(master,orient=VERTICAL)
		zipcodeScrollbar.grid(row = 6, column = 5, sticky = N+S+W+E)
		self.zipcodeListbox = Listbox(master, listvariable=zipcodes, selectmode='multiple', width=40,height =5)
		self.zipcodeListbox.configure(yscrollcommand=zipcodeScrollbar.set)
		zipcodeScrollbar.config(command=self.zipcodeListbox.yview())
		addZipButton = ttk.Button(master, text='Add Zipcode', command = self.addZip)
		prefZipLabel = ttk.Label(master,text= "Preferred Zipcodes",style="Header.TLabel")
		removeZipButton = ttk.Button(master,text='Remove Selected Zipcodes',command = lambda: self.removeZips(self.zipcodeListbox.curselection()))

		header.grid(row=0,column=0)
		scoreCheckbox.grid(row=1,column=0)
		scheduleCheckbox.grid(row=2,column=0)
		weatherCheckbox.grid(row=3,column=0)

		spacerHorz.grid(row=0,column=1,padx=10,pady=50)

		allTeamLabel.grid(row=0,column=2)
		allTeamListbox.grid(row=1,column=2)
		spacer_frame.grid(row=2,column=5,pady=2)
		teamEntryLabel.grid(row=3,column=2)
		self.teamEntry.grid(row=4,column=2)
		addTeamButton.grid(row=5,column=2)
		prefNBATeamLabel.grid(row=6,column=2)
		self.teamListbox.grid(row=7,column=2)
		removeTeamButton.grid(row=8,column=2)

		spacerHorz.grid(row=0,column=3,padx=10,pady=50)

		ttk.Label(master,text = 'Forecast Info', style='Header.TLabel').grid(row=0,column=4,pady=1)
		unitEntryLabel.grid(row = 1, column=4)
		unitEntry.grid(row=2,column=4)
		zipEntryLabel.grid(row=3,column=4)
		self.zipcodeEntry.grid(row=4,column=4)
		addZipButton.grid(row=5,column=4)
		prefZipLabel.grid(row=6,column=4)
		self.zipcodeListbox.grid(row=7,column=4)
		removeZipButton.grid(row=8,column=4)

	def buildGuiSender(self, master, senderEmailVar,senderPasswordVar):
		header = ttk.Label(master, text = 'Sender Credentials:', style = 'Header.TLabel')
		emailLabel = ttk.Label(master, text = "Email:")
		emailEntry = ttk.Entry(master, width = 40,textvariable = senderEmailVar)
		passwordLabel = ttk.Label(master, text = 'Password:')
		passwordEntry = ttk.Entry(master, width = 40, show = '*', textvariable = senderPasswordVar)
		header.grid(row = 0, column = 0, columnspan = 2)
		emailLabel.grid(row = 1, column = 0, pady = 2, sticky = E)
		emailEntry.grid(row = 1, column = 1, pady = 2, sticky = W)
		passwordLabel.grid(row = 2, column = 0, pady = 2, sticky = E)
		passwordEntry.grid(row = 2, column = 1, pady = 2, sticky = W)   
		

	def buildGuiControls(self,master):
		updateButton = ttk.Button(master, text = 'Update Preferences', command = self.updatePreferences)
		sendButton = ttk.Button(master, text = 'Manual Send', command = self.manualSend)
		updateButton.grid(row = 0, column = 0)
		sendButton.grid(row = 0, column = 1)

	def addRecipient(self):
		newRecip = self.recipientsEntry.get()
		if newRecip !="":
			self.rInd+=1
			self.recipientsListbox.insert(self.rInd,newRecip+"")
			self.recipientsEntry.delete(0,END) #clears entry
			
	def removeRecipients(self,selection):
		recipList = list(self.recipList.get())
		for i in reversed(selection):
			#removes from recipList and the user info dict in the same line
			self.__email.recipients.pop(recipList.pop(i))
		self.recipList.set(recipList)

	#use insert and an iterator int var
	def addTeam(self):
		newTeam = self.teamEntry.get()
		if newTeam !='':
			self.tInd+=1
			self.teamListbox.insert(self.tInd,newTeam)
			self.teamEntry.delete(0,END) #clears the entry
	
	def removeTeams(self,selection):
		teamList = list(self.teamList.get())
		for i in reversed(selection):
			teamList.pop(i)
		self.teamList.set(teamList)

	def addZip(self):
		newZip = self.zipcodeEntry.get()
		if newZip !='':
			self.zInd+=1
			self.zipcodeListbox.insert(self.zInd,newZip)
			self.zipcodeEntry.delete(0,END) #clears entry

	def removeZips(self,selection):
		zipList = list(self.zipList.get())
		for i in reversed(selection):
			zipList.pop(i)
		self.zipList.set(zipList)

	def updatePreferences(self):
		self.addRecipient()
		#later try get rid of duplicates in rList if certain users have updated info
		rList = self.recipList.get()
		#adds to dictionary of users and their preferred info in email class, makes only the necessary arrays
		self.__email.recipients[rList[len(rList)-1]]=[[self.scoreVar.get(),self.scheduleVar.get(),self.weatherVar.get()],list(self.teamList.get()) if self.scoreVar.get() or self.scheduleVar.get() else [],[self.unitVar.get(),list(self.zipList.get())] if self.weatherVar.get() else []]
		print(self.__email.recipients)
		self.tInd=0
		self.zInd=0
		self.__email.senderInfo = {'email':self.senderEmailVar.get(),'password':self.senderPasswordVar.get()}
		self.teamListbox.delete(0,END)
		self.zipcodeListbox.delete(0,END)
		self.saveConfig()
		

	#program shuts down after sending emails and saving the info for them
	def manualSend(self):
		self.__email.sendEmail()
		self.running = False
	
	def saveConfig(self,filePath='wanbarConfig.json'):
		config = self.__email.recipients
		#appends user info #it works
		with open(filePath,'w') as file:
			json.dump(config,file,indent=4)	

#uncomment #root.mainloop() to run interface and input new info or change old info
if __name__ == "__main__":
	root = Tk()
	app = emailGUI(root)
	root.mainloop()
	"""while app.running:
		app.manualSend()
		app.running = False"""
	os._exit(0)

