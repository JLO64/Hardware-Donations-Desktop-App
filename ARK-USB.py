import os, sys, glob
sys.path.append("Python_Functions")
import terminalColor

terminalColor.printGreenString("STARTING PROGRAM...\n")
#os.system("./ARK-OS_Installer")

#list files
#print(glob.glob("ARK-OS/*"))


print("What do you want to do?")
intDecision = 0
while ( (intDecision < 1) or (intDecision > 4) ):
    try:
        terminalColor.printBlueString("1. Flash a hard drive\n2. Upgrade a system with ARK-OS\n3. Download files\n4. Exit")
        intDecision = int(input())
        if ( (intDecision < 1) or (intDecision > 4) ):
            terminalColor.printRedString("Invalid Input")
    except:
        intDecision = 0
        terminalColor.printRedString("Invalid Input")
