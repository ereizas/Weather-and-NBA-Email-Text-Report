# Synopsis
This program is meant to send an email at a certain time to each client with the yesterday scores and/or today's schedule for preferred NBA teams, and/or weather forecast for the day for preferred zip codes. To schedule this to run everyday automatically, follow the instructions for setting up the program with task manager.

# Setup

## Python

1. Go to https://www.python.org/downloads/ and click the button that says "Download Python"
2. Click on the exe installer for Python and if there is a box that says something about adding to PATH, check it, allow permission to override path length at the end of the click through and skip to step 4. Click through to continue and make sure you know where it is downloaded to
3. Click through to continue and make sure you copy the path where it is downloaded to
4. Set the path by following the instructions for whichever system you use:
Windows - https://www.tutorialspoint.com/How-to-set-python-environment-variable-PYTHONPATH-on-Windows#:~:text=Set%20PYTHONPATH%20using%20Command%20Prompt&text=Click%20on%20the%20%22Environment%20Variables,to%20save%20the%20environment%20variable.
Linux - https://www.tutorialspoint.com/How-to-set-python-environment-variable-PYTHONPATH-on-Linux#:~:text=By%20setting%20the%20PYTHONPATH%20environment,of%20the%20default%20search%20paths.
Mac - https://www.educative.io/answers/how-to-add-python-to-the-path-variable-in-mac

## Task Scheduler

This step is essential for getting the program to run everyday at a certain time. (I will write out how to do this for Windows, but for Mac and Linux, if you do not know how to schedule a program to run everyday, you will have to look up how or try it yourself based on what I present here and intuition). *Note: The computer you set this up on, must be on at the time or some point afterward to be able to automatically send emails. 

1. Go to Task Scheduler or search up "Task Scheduler" in you Application/Start search bar
2. Click on the "Task Scheduler Library" tab on the left
3. Click "Create Task" on the right side
4. Name the task something that you would be able to remember or spot easily as the automated email task (i.e. "Daily Email Report")
5. Decide whether you want the program to run whether the user is logged on or not or only when user is logged on (if you can't decide just leave it as the default option)
6. Click on the "Triggers" tab and click "New..."
7. Make sure that next to "Begin the task:", it says "On a schedule"
8. Pick the start date and start time (click "Synchronize across time zones" if you would like)
9. Click the bubble next to "Daily" and make sure that "1" is in the blank for "Recur every: _ days"
10. Click "OK" and click on the "Actions" tab
11. Click "New..." and make sure next to "Action:" it says "Start a program"
12. Under "Program/script" paste the path that you copied when setting up Python
13. In the box to the right of "Add arguments (optional):" type "gui.py"
14. In the box to the right of "Start in (optional):" paste the path of the folder you downloaded the project to

## Bot Email

It is necessary to follow these steps to create a bot gmail account and an app password for the account so that the program can log in without error.

1. Create a gmail address that you want to send the daily emails
2. Click on the Google profile picture and click "Manage your Google Account"
3. Click on the "Security" tab on the left and click on "2-Step Verification" under "How you sign in to Google"
4. Go through the setup
5. When you are done, go back into 2-Step Verification if you are not already there, scroll down, and click on "App passwords"
6. Click on "Select app" and click "Mail"
7. Click on "Select device" and click the device that matches what you will run this program on or "Other (Custom name)" if you do not see your device
8. Copy the app password that appears in the colored box and go to the keys_and_passwords.py where you have the project downloaded to
9. Paste the app password into the quotation marks next to "password"
10. Type in or paste the email address of the new account into the quotation marks next to "emailAddr" in the same file

## OpenWeather API Password

This step is necessary for being able to access weather forecast information.

1. Go to https://home.openweathermap.org/users/sign_up if you do not have an account with OpenWeather API, otherwise if you already have an account skip to step 3
2. Do the necessary verification to create your account (when asked about company and purpose, skip the company entry and select other for purpose, then verify the email)
3. Sign in
4. Click on your username (or partial username) in the top right corner of the page
5. Click "My API Keys" and copy the key under "Key"
6. Go to the keys_and_passwords.py file where you downloaded the project and paste the key in the quotation marks next to apiKey

# Installing and Running

1. On the github page, click the green button that says "Code" and then "Download zip"
2. Find the zip file, right click on it, extract it to a desired folder, and copy the full path of the extracted folder (should look something like "C:.../desired_folder/Appropriate-Song-Separator")
3. Open up the terminal/command prompt
4. Change the directory to the folder that was extracted by typing "cd" and pasting the path you copied earlier (CTRL + SHIFT + V) and pressing Enter
5. Type or paste "py -3 -m venv .venv" and press Enter (after you do this once for the project you won't have to do it again)
6. Type or paste ".venv/scripts/activate" (This step and step 11 will have to be done everytime you open up a new terminal to run a program that has installed a virtual environement by doing step 8)
7. Type or paste "pip install -r requirements.txt" and press Enter 
8. To run the program, type "python gui.py" and press Enter
9. Enter the appropriate information and pay attention to the text box at the bottom for info about the program's run. If you see a YouTube or Spotify link pop in the text box, there might also be a website that pops up on your browser. Make sure these links match or at least make sure the links are Spotify or YouTube links and allow all permissions.

# wanbarConfig.json Format

Instead of using the GUI to make small changes to the wanbarConfig.json file which the program looks at to decide who to email what, if you know the format of the file, you can make small changes yourself. (Bool=True or False value)


{
    emailAddress:
    [
        [
            userWantsNBAScoresBool,
            userWantsNBAScheduleBool,
            userWantsWeatherForecastBool
        ],
        [
            '76ers','Bucks','Bulls','Cavaliers','Celtics','Clippers','Grizzlies','Hawks','Heat','Hornets','Jazz','Kings','Knicks','Lakers',
		    'Magic','Mavericks','Nets','Nuggets','Pacers','Pelicans','Pistons','Raptors','Rockets','Spurs','Suns','Thunder','Timberwolves','Trail Blazers','Warriors','Wizards (These are just to show how to enter the team names, i.e. must enter 76ers not Sixers for the Philly team)' 
        ],
        [
            0 for imperial, 1 for metric, or 2 for standard (can only choose one for each user),
            [
                'zipcode'
            ]
        ]

    ],
    emailAddress2:...
}

# Ideas for Future Capabilities

HTML formatted emails for a more aesthetically pleasing email
Include different sports leagues
