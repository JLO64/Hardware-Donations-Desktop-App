import terminalColor, fileFunctions, settingsJson, browseDatabase
import json, os

def changeSettings():
    intDecision = 0
    listOfOptions =[". GUI Mode", ". Color Mode", ". Account Settings", ". Version Info", ". Cancel"]
    while ( ( (intDecision < 1) or (intDecision > len(listOfOptions)) ) ):
        try:
            print("\nWhat settings do you want to change?")
            for i in range( len(listOfOptions) ):
                terminalColor.printBlueString( str(i+1) + listOfOptions[i] )
            intDecision = int(input())
            if ( (intDecision < 1) or (intDecision > len(listOfOptions)) ):
                terminalColor.printRedString("Invalid Input")
            elif ( listOfOptions[intDecision-1] == ". Cancel"): #Exit program
                break
            elif ( listOfOptions[intDecision-1] == ". GUI Mode"):
                intDecision = 0
                changeGUI()
            elif ( listOfOptions[intDecision-1] == ". Color Mode"):
                intDecision = 0
                changeColor()
            elif ( listOfOptions[intDecision-1] == ". Account Settings"):
                intDecision = 0
                if browseDatabase.hasValidCredStored(): accountSettings(False)
                else: accountSettings(True)
            elif ( listOfOptions[intDecision-1] == ". Version Info"):
                intDecision = 0
                print("\nHardware-Donations Desktop App\nVersion Pre-Production\nBuilt With Python 3.6.9\n")
            else:
                intDecision = 0    
        except:
            intDecision = 0
            terminalColor.printRedString("Invalid Input")

def changeGUI():
    intDecision = 0
    listOfOptions =[". Yes(Default)", ". No", ". Cancel"]
    while ( ( (intDecision < 1) or (intDecision > len(listOfOptions)) ) ):
        try:
            print("\nDo you want GUI Mode to be ON? If turned off file paths will have to be entered manually.")
            if settingsJson.guiMode == True: print("Currently GUI Mode is ON")
            else: print("Currently GUI Mode is OFF")

            for i in range( len(listOfOptions) ):
                terminalColor.printBlueString( str(i+1) + listOfOptions[i] )
            intDecision = int(input())
            if ( (intDecision < 1) or (intDecision > len(listOfOptions)) ):
                terminalColor.printRedString("Invalid Input")
            elif ( listOfOptions[intDecision-1] == ". Cancel"):
                break
            elif ( listOfOptions[intDecision-1] == ". Yes(Default)"):
                settingsJson.guiMode = True
                writeJSONSettings()
            elif ( listOfOptions[intDecision-1] == ". No"):
                settingsJson.guiMode = False
                writeJSONSettings()
            else:
                intDecision = 0    
        except:
            intDecision = 0
            terminalColor.printRedString("Invalid Input")
    terminalColor.printGreenString("SETTINGS UPDATED")

def changeColor():
    intDecision = 0
    listOfOptions =[". Yes(Default)", ". No", ". Cancel"]
    while ( ( (intDecision < 1) or (intDecision > len(listOfOptions)) ) ):
        try:
            print("\nDo you want Color Mode to be ON? If turned off it is harder to use the terminal interface.")
            if settingsJson.colorMode == True: print("Currently Color Mode is ON")
            else: print("Currently Color Mode is OFF")

            for i in range( len(listOfOptions) ):
                terminalColor.printBlueString( str(i+1) + listOfOptions[i] )
            intDecision = int(input())
            if ( (intDecision < 1) or (intDecision > len(listOfOptions)) ):
                terminalColor.printRedString("Invalid Input")
            elif ( listOfOptions[intDecision-1] == ". Cancel"):
                break
            elif ( listOfOptions[intDecision-1] == ". Yes(Default)"):
                settingsJson.colorMode = True
                writeJSONSettings()
            elif ( listOfOptions[intDecision-1] == ". No"):
                settingsJson.colorMode = False
                writeJSONSettings()
            else:
                intDecision = 0    
        except:
            intDecision = 0
            terminalColor.printRedString("Invalid Input")
    terminalColor.printGreenString("SETTINGS UPDATED")

def writeJSONSettings():
    fileFunctions.checkForDirectory( os.path.expanduser('~') + "/HardwareDonations/Settings" )
    data = {}
    data["GUImode"] = settingsJson.guiMode
    data["colorMode"] = settingsJson.colorMode
    with open( os.path.expanduser('~') + "/HardwareDonations/Settings/Settings", 'w') as outfile:
        json.dump(data, outfile)

def readJSONSettings():
    if fileFunctions.checkForFile(os.path.expanduser('~') + "/HardwareDonations/Settings/Settings"):
        with open(os.path.expanduser('~') + "/HardwareDonations/Settings/Settings") as json_file:
            data = json.load(json_file)
            return data
    else: 
        writeJSONSettings()
        data = {}
        return data

def initializeSettings():
    data = readJSONSettings()
    if( not data == {} ):
        if(not settingsJson.guiMode == False): settingsJson.guiMode = data["GUImode"]
        settingsJson.colorMode = data["colorMode"]

def logoutOfAccount():
    intlogoutDecision = 0
    listOfLogoutOptions =[". Yes", ". No"]
    while intlogoutDecision == 0:
        print("Do you want to logout of your account?")
        for i in range( len(listOfLogoutOptions) ):
            terminalColor.printBlueString( str(i+1) + listOfLogoutOptions[i] )
        intlogoutDecision = int(input())
        if ( (intlogoutDecision < 1) or (intlogoutDecision > len(listOfLogoutOptions)) ):
            terminalColor.printRedString("Invalid Input")
        elif ( listOfLogoutOptions[intlogoutDecision-1] == ". No"): #Exit program
            pass
        elif ( listOfLogoutOptions[intlogoutDecision-1] == ". Yes"):
            settingsJson.key1 = "na"
            settingsJson.key2 = "na"
            settingsJson.key3 = "na"
            fileFunctions.deleteFile(os.path.expanduser('~') + "/HardwareDonations/Settings/LoginInfo")
            terminalColor.printGreenString("SETTINGS UPDATED")

def accountSettings(isLoggedOut):
    if isLoggedOut:
        isLoggedOut = not browseDatabase.askForCredentials()
    if not isLoggedOut:
        intDecision = 0
        listOfOptions =[". Logout", ". Change Password", ". Cancel"]
        while ( ( (intDecision < 1) or (intDecision > len(listOfOptions)) ) ):
            try:
                print("\nWhat settings do you want to change?")
                for i in range( len(listOfOptions) ):
                    terminalColor.printBlueString( str(i+1) + listOfOptions[i] )
                intDecision = int(input())
                if ( (intDecision < 1) or (intDecision > len(listOfOptions)) ):
                    terminalColor.printRedString("Invalid Input")
                elif ( listOfOptions[intDecision-1] == ". Cancel"): #Exit program
                    break
                elif ( listOfOptions[intDecision-1] == ". Logout"):
                    logoutOfAccount()
            except:
                intDecision = 0
                terminalColor.printRedString("Invalid Input")