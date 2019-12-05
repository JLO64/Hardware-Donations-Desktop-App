# Hardware Donations Desktop App

## Install Dependencies

Run ```pip3 install -r requirements.txt``` in the terminal in the directory where all of the files are located.

## Generating An Executible File

In the directory where ```Hardware-Donations.py``` is located run ```pyinstaller Hardware-Donations.py -F -p Python_Functions/```

A new "dist" directory will be generated and the executible file will be there.

## Install System-Wide (Linux)
Copy the executible file to the ```/usr/local/bin``` directory. You will need sudo privalages for this command. To run the program just type in ```Hardware-Donations``` from any directory in the terminal.