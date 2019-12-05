import os, sys, glob
sys.path.append("Python_Functions")
import terminalColor, downloadFiles, fileFunctions

terminalColor.printGreenString("STARTING PROGRAM...\n")
fileFunctions.checkForDirectory(os.path.expanduser('~') + "/HardwareDonations")
#os.system("./ARK-OS_Installer")

#list files
#print(glob.glob("ARK-OS/*"))

if __name__ == "__main__":
    intDecision = 0
    listOfOptions =[". Flash a hard drive", ". Upgrade a system with ARK-OS", ". Download files", ". Exit"]
    while ( ( (intDecision < 1) or (intDecision > 4) ) ):
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
                downloadFiles.downloadFilesMain()
            else:
                intDecision = 0    
        except:
            intDecision = 0
            terminalColor.printRedString("Invalid Input")