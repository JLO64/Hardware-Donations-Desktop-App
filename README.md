# Hardware Donations Desktop App

## Clone The Repository (Linux)

On Linux to clone the repository open the terminal and go to the directory where you wish to clone(download) it. Then type```git clone https://github.com/JLO64/Hardware-Donations-Desktop-App.git```

## Install Dependencies

First make sure that you have Python3 installed.  On linux you can just type ```python3``` into the terminal and it will show you what version you have of it installed.

Then install ```pip```, on Debian based systems all you have to do is run ```sudo apt install python3-pip```

Finally, run ```pip3 install -r requirements.txt``` in the terminal in the directory where ```Hardware-Donations.py``` is located

## Generating An Executible File

In the directory as above run ```pyinstaller Hardware-Donations.py -F -p Python_Functions/```

A new "dist" directory will be generated and the executible file will be there.

## Install System-Wide (Linux)
Copy the executible file to the ```/usr/bin``` directory. You will need sudo privalages for this command. To run the program just type in ```Hardware-Donations``` in the terminal.
