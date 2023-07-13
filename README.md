# Synopsis
This program is meant to send an email at a certain time to each client with the yesterday scores and/or today's schedule for preferred NBA teams, and/or weather forecast for the day for preferred zip codes. To schedule this to run everyday automatically, follow the instructions for setting up the program with task manager.

# Installing and Running

1. If you have Python and have set up the path environment variable for it, skip to step 4. Otherwise, go to https://www.python.org/downloads/ and click the button that says "Download Python"
2. Click on the exe installer for Python and click through to continue and make sure you know where it is downloaded to
3. Set the path by following the instructions for whichever system you use:
Windows - https://www.tutorialspoint.com/How-to-set-python-environment-variable-PYTHONPATH-on-Windows#:~:text=Set%20PYTHONPATH%20using%20Command%20Prompt&text=Click%20on%20the%20%22Environment%20Variables,to%20save%20the%20environment%20variable.
Linux - https://www.tutorialspoint.com/How-to-set-python-environment-variable-PYTHONPATH-on-Linux#:~:text=By%20setting%20the%20PYTHONPATH%20environment,of%20the%20default%20search%20paths.
Mac - https://www.educative.io/answers/how-to-add-python-to-the-path-variable-in-mac
4. On the github page, click the green button that says "Code" and then "Download zip"
5. Find the zip file, right click on it, extract it to a desired folder, and copy the full path of the extracted folder (should look something like "C:.../desired_folder/Appropriate-Song-Separator")
6. Open up the terminal/command prompt
7. Change the directory to the folder that was extracted by typing "cd" and pasting the path you copied earlier (CTRL + SHIFT + V) and pressing Enter
8. Type or paste "py -3 -m venv .venv" and press Enter (after you do this once for the project you won't have to do it again)
9. Type or paste ".venv/scripts/activate" (This step and step 11 will have to be done everytime you open up a new terminal to run a program that has installed a virtual environement by doing step 8)
10. Type or paste "pip install -r requirements.txt" and press Enter 
11. To run the program, type "python gui.py" and press Enter
12. Enter the appropriate information and pay attention to the text box at the bottom for info about the program's run. If you see a YouTube or Spotify link pop in the text box, there might also be a website that pops up on your browser. Make sure these links match or at least make sure the links are Spotify or YouTube links and allow all permissions.

# wanbarConfig.json Format

# Ideas for Future Capabilities

HTML formatted emails for a more aesthetically pleasing email
Include different sports leagues
