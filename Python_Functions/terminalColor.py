import settingsJson

class bcolors:
    HEADER = '\033[95m'
    BLUE = '\033[1;34m'
    CYAN = '\033[0;36m'
    YELLOW = '\033[0;33m'
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

def printCyanString( stringToPrint ):
    if settingsJson.colorMode == True: print( bcolors.CYAN + stringToPrint + bcolors.ENDC )
    else: print(stringToPrint)

def printYellowString( stringToPrint ):
    if settingsJson.colorMode == True: print( bcolors.YELLOW + stringToPrint + bcolors.ENDC )
    else: print(stringToPrint)

def generateRedString( stringToPrint ):
    if settingsJson.colorMode == True: return bcolors.RED + stringToPrint.upper() + bcolors.ENDC 
    else: return(stringToPrint.upper())

def generateGreenString( stringToPrint ):
    if settingsJson.colorMode == True: return( bcolors.GREEN + stringToPrint.upper() + bcolors.ENDC )
    else: return(stringToPrint.upper())

def generateBlueString( stringToPrint ):
    if settingsJson.colorMode == True: return( bcolors.BLUE + stringToPrint + bcolors.ENDC )
    else: return(stringToPrint)

def generateCyanString( stringToPrint ):
    if settingsJson.colorMode == True: return( bcolors.CYAN + stringToPrint + bcolors.ENDC )
    else: return(stringToPrint)

def generateYellowString( stringToPrint ):
    if settingsJson.colorMode == True: return( bcolors.YELLOW + stringToPrint + bcolors.ENDC )
    else: return(stringToPrint)