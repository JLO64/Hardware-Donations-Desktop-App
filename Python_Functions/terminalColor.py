import settingsJson

class bcolors:
    HEADER = '\033[95m'
    BLUE = '\033[1;34m'
    GREEN = '\033[1;32m'
    RED = '\033[1;31m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def printRedString( stringToPrint ):
    if settingsJson.colorMode == True: print( bcolors.RED + stringToPrint.upper() + bcolors.ENDC )
    else: print(stringToPrint.upper())

def printGreenString( stringToPrint ):
    if settingsJson.colorMode == True: print( bcolors.GREEN + stringToPrint.upper() + bcolors.ENDC )
    else: print(stringToPrint.upper())

def printBlueString( stringToPrint ):
    if settingsJson.colorMode == True: print( bcolors.BLUE + stringToPrint + bcolors.ENDC )
    else: print(stringToPrint)