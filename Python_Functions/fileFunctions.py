import sys, os, urllib.request

def checkForDirectory(programPath): #checks for "programPath" directory and creates it if not found
    if not os.path.exists(programPath):
        os.makedirs(programPath)
    return programPath

def internet_on():
    for timeout in [1,5,10,15]:
        try:
            response=urllib.request.urlopen('http://google.com',timeout=timeout)
            return True
        except: pass
    return False