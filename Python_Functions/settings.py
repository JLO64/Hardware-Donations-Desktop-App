import terminalColor, fileFunctions, settingsJson
import json, os

def changeSettings():
    intDecision = 0
    listOfOptions =[". GUI Mode", ". Exit"]
    while ( ( (intDecision < 1) or (intDecision > len(listOfOptions)) ) ):
        try:
            print("What settings do you want to change?")
            for i in range( len(listOfOptions) ):
                terminalColor.printBlueString( str(i+1) + listOfOptions[i] )
            intDecision = int(input())
            if ( (intDecision < 1) or (intDecision > len(listOfOptions)) ):
                terminalColor.printRedString("Invalid Input")
            elif ( listOfOptions[intDecision-1] == ". Exit"): #Exit program
                break
            elif ( listOfOptions[intDecision-1] == ". GUI Mode"):
                intDecision = 0
                changeGUI()
            else:
                intDecision = 0    
        except:
            intDecision = 0
            terminalColor.printRedString("Invalid Input")

def changeGUI():
    global guiMode

    intDecision = 0
    listOfOptions =[". Yes(Default)", ". No", ". Cancel"]
    while ( ( (intDecision < 1) or (intDecision > len(listOfOptions)) ) ):
        try:
            print("Do you want GUI mode to be ON? If turned off file paths will have to be entered manually.")
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

def writeJSONSettings():
    fileFunctions.checkForDirectory( os.path.expanduser('~') + "/HardwareDonations/Settings" )
    data = {}
    data["GUImode"] = settingsJson.guiMode
    with open( os.path.expanduser('~') + "/HardwareDonations/Settings/Settings.txt", 'w') as outfile:
        json.dump(data, outfile)

def readJSONSettings():
    if fileFunctions.checkForFile(os.path.expanduser('~') + "/HardwareDonations/Settings/Settings.txt"):
        with open(os.path.expanduser('~') + "/HardwareDonations/Settings/Settings.txt") as json_file:
            data = json.load(json_file)
            return data
    else: 
        writeJSONSettings()
        data = {}
        return data

def initializeSettings():
    data = readJSONSettings()
    if( not data == {} ):
        settingsJson.guiMode = data["GUImode"]   