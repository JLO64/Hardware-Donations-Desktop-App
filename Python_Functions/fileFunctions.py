import sys, os

def checkForDirectory(programPath): #checks for "Hardware_Donations" directory and creates it if not found
    if not os.path.exists(programPath):
        os.makedirs(programPath)