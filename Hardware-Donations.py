import os, sys, glob
sys.path.append("Python_Functions")
import terminalColor, downloadFiles, fileFunctions, settings, settingsJson

terminalColor.printGreenString("STARTING PROGRAM...")
fileFunctions.checkForDirectory(os.path.expanduser('~') + "/HardwareDonations")
settings.initializeSettings()
terminalColor.printGreenString("SETTINGS LOADED!\n")

#os.system("./ARK-OS_Installer")
#print(glob.glob("ARK-OS/*")) #list files

if __name__ == "__main__":
    intDecision = 0
    listOfOptions =[". Flash a hard drive", ". Upgrade a system with ARK-OS", ". Download files", ". Settings", ". Exit"]
    while ( ( (intDecision < 1) or (intDecision > len(listOfOptions)) ) ):
        try:
            print("What do you want to do?")
            for i in range( len(listOfOptions) ):
                terminalColor.printBlueString( str(i+1) + listOfOptions[i] )
            intDecision = int(input())
            if ( (intDecision < 1) or (intDecision > len(listOfOptions)) ):
                terminalColor.printRedString("Invalid Input")
            elif ( listOfOptions[intDecision-1] == ". Exit"): #Exit program
                break
            elif ( listOfOptions[intDecision-1] == ". Download files"): #Download files
                intDecision = 0
                if (fileFunctions.internet_on() == True):
                    downloadFiles.downloadFilesMain()
                else:
                    terminalColor.printRedString("Unable to connect to internet")
            elif ( listOfOptions[intDecision-1] == ". Settings"): #Settings
                intDecision = 0
                settings.changeSettings()
            else:
                intDecision = 0    
        except:
            intDecision = 0
            terminalColor.printRedString("Invalid Input")