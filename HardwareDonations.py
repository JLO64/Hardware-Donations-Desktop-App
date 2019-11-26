import os, sys, glob
sys.path.append("Python_Functions")
import terminalColor, downloadFiles, fileFunctions

terminalColor.printGreenString("STARTING PROGRAM...\n")
fileFunctions.checkForDirectory(os.path.expanduser('~') + "/HardwareDonations")
#os.system("./ARK-OS_Installer")

#list files
#print(glob.glob("ARK-OS/*"))

intDecision = 0
terminateLoop = False
while ( ( (intDecision < 1) or (intDecision > 4) ) or (terminateLoop == False) ):
    try:
        print("What do you want to do?")
        terminalColor.printBlueString("1. Flash a hard drive\n2. Upgrade a system with ARK-OS\n3. Download files\n4. Exit")
        intDecision = int(input())
        if ( (intDecision < 1) or (intDecision > 4) ):
            terminalColor.printRedString("Invalid Input")
        elif (intDecision == 4): #Exit program
            terminateLoop = True
        elif (intDecision == 3): #Download files
            downloadFiles.downloadFilesMain()
    except:
        intDecision = 0
        terminalColor.printRedString("Invalid Input")