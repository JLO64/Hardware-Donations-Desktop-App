# ARK-USB-Files

## Dependencies To Import

Run ```pip install request``` or ```pip3 install request```

(Depends on whether or not you are using Python3.)

## How To Generate An Executible File

Install PyInstaller by running ```pip install PyInstaller```

(run ```pip3 install PyInstaller``` if you used ```pip3```)

Then in the directory where ```HardwareDonations.py``` is located run ```pyinstaller ARK-USB.py -F -p Python_Functions/```

A new "dist" directory will be generated and the executible file will be there.

### Install System-Wide (Linux)
Copy the executible file to the ```/usr/local/bin``` directory. You will need sudo privalages for this command.