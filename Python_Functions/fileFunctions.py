import sys, os

def checkForDirectory(programPath): #checks for "programPath" directory and creates it if not found
    if not os.path.exists(programPath):
        os.makedirs(programPath)