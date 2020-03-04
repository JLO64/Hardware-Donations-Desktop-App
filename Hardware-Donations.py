import os, sys, glob, webbrowser, io, time
sys.path.append("Python_Functions")
import terminalColor, downloadFiles, fileFunctions, settings, settingsJson, browseDatabase

#os.system("./ARK-OS_Installer")
#print(glob.glob("ARK-OS/*")) #list files

def printARKDino():
    arkDino = "\n     ╓╫╫╫╫╫╫╫╫╓\n     ╫╫╫╫╫╫╫╫╫╫\n     ╙╫╫╫╫╫╫╫╫╫\n          ╫╫╫╫╫\n          ╫╫╫╫╫╥\n          ╫╫╫╫╫╫╦╕\n        ╙╙╫╫╫╫╫╫╫╫╫╦        ╦\n           ║╫╫╫╫╫╫╫╫╫╦╥  ╓╥╫╫\n             ╩╫╫╫╫╫╫╫╫╫╫╫╫╫╫\n              └╫╫╫╫╫╫╫╫╫╫╫╩└\n                ╞╫╫╙╫╫╫╙\n               ╥║╡  ╥║╫\n"
    print(arkDino + "\nHardware Donations Desktop App v" + str(settingsJson.versionNum) + "\n\n")

if __name__ == "__main__":
    terminalColor.printGreenString("STARTING PROGRAM...")
    fileFunctions.checkForDirectory(os.path.expanduser('~') + "/HardwareDonations")
    settings.initializeSettings()
    terminalColor.printGreenString("SETTINGS LOADED!")
    printARKDino()

    intDecision = 0
    listOfOptions =[". Install ARK-OS", ". Access Database", ". Download Files", ". Go To Youtube Channel", ". Settings", ". Exit"]
    while ( ( (intDecision < 1) or (intDecision > len(listOfOptions)) ) ):
        try:
            print("\nWhat do you want to do?")
            for i in range( len(listOfOptions) ): terminalColor.printBlueString( str(i+1) + listOfOptions[i] )
            intDecision = int(input())
            if ( (intDecision < 1) or (intDecision > len(listOfOptions)) ): terminalColor.printRedString("Invalid Input")
            elif ( listOfOptions[intDecision-1] == ". Exit"): break #Exit program
            elif ( listOfOptions[intDecision-1] == ". Download Files"):
                intDecision = 0
                if (fileFunctions.internet_on() == True): downloadFiles.downloadFilesMain()
                else: terminalColor.printRedString("Unable to connect to internet")
            elif ( listOfOptions[intDecision-1] == ". Download Files"):
                intDecision = 0
                if (fileFunctions.internet_on() == True): downloadFiles.downloadFilesMain()
                else: terminalColor.printRedString("Unable to connect to internet")
            elif ( listOfOptions[intDecision-1] == ". Access Database"):
                intDecision = 0
                if (fileFunctions.internet_on() == True): browseDatabase.loginToAWS()
                else: terminalColor.printRedString("Unable to connect to internet")
            elif ( listOfOptions[intDecision-1] == ". Settings"):
                intDecision = 0
                settings.changeSettings()
            elif ( listOfOptions[intDecision-1] == ". Go To Youtube Channel"):
                intDecision = 0
                terminalColor.printGreenString("\nopening youtube")
                webbrowser.open("https://www.youtube.com/channel/UCKd1F6Tbmgqhnt2bADXCCTg", new=0, autoraise=True)
                time.sleep(0.7)
            else:
                intDecision = 0    
        except:
            intDecision = 0
            terminalColor.printRedString("Invalid Input")