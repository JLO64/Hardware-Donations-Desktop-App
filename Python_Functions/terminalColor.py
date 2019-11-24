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
    print( bcolors.RED + stringToPrint + bcolors.ENDC )

def printGreenString( stringToPrint ):
    print( bcolors.GREEN + stringToPrint + bcolors.ENDC )

def printBlueString( stringToPrint ):
    print( bcolors.BLUE + stringToPrint + bcolors.ENDC )