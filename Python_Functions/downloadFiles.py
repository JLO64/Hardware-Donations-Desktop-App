import os, sys, json, urllib.request
import terminalColor, fileFunctions, settingsJson
import array as arr
try:
    from tkinter import *
    from tkinter import filedialog
except:
    settingsJson.guiMode = False
    pass

def downloadFilesMain():
    downloadFilesList()
    readFileList()

def downloadFilesList():
    terminalColor.printGreenString("\nDownloading list of files")
    url = "https://hardware-donations-database-gamma.s3-us-west-1.amazonaws.com/Misc_Items/DownloadList"
    urllib.request.urlretrieve(url, os.path.expanduser('~') + "/HardwareDonations/Settings/DownloadList" )
    terminalColor.printGreenString("Download Finished")

def chooseFolderToSaveFile( downloadInfo ):
    if(downloadInfo[1] == "none" ):
        return
    else:
        fileLoc = ""
        if( settingsJson.guiMode == True ):
            root = Tk()
            root.withdraw()
            options = {} #https://www.programcreek.com/python/example/9924/tkFileDialog.asksaveasfilename
            options['title'] = "Download As"
            options['initialfile'] = downloadInfo[1]
            
            if( downloadInfo[2] == ".txt" ):
                options['filetypes'] = [('text files', '.txt')]
            elif( downloadInfo[2] == ".pdf" ):
                options['filetypes'] = [('pdf files', '.pdf')]
            elif( downloadInfo[2] == ".zip" ):
                options['filetypes'] = [('zip files', '.zip')]
            elif( downloadInfo[2] == ".png" ):
                options['filetypes'] = [('png files', '.png')]

            if( downloadInfo[3] == "PDFs" ):
                options['initialdir'] = fileFunctions.checkForDirectory(os.path.expanduser('~') + "/HardwareDonations/PDF_Files")
            elif( downloadInfo[3] == "Legal" ):
                options['initialdir'] = fileFunctions.checkForDirectory(os.path.expanduser('~') + "/HardwareDonations/Legal_Files")
            elif( downloadInfo[3] == "Photos" ):
                options['initialdir'] = fileFunctions.checkForDirectory(os.path.expanduser('~') + "/HardwareDonations/Photos")
            elif( downloadInfo[3] == "Wallpapers" ):
                options['initialdir'] = fileFunctions.checkForDirectory(os.path.expanduser('~') + "/HardwareDonations/Wallpapers")
                
            fileLoc = filedialog.asksaveasfilename(**options)
        elif(settingsJson.guiMode == False):
            validDirPath = False
            while validDirPath == False:
                print("Please type the path of the directory you want to save to.(Or type \"Cancel\")")
                fileLoc = str(input())
                if fileLoc.lower() == "cancel":
                    break
                elif not ( "/" == fileLoc[-1] and os.path.exists(fileLoc) ):
                    terminalColor.printRedString("Invalid directory")
                else:
                    validDirPath = True
        if ( len(fileLoc) > 0 ) and not (fileLoc.lower() == "cancel"):
            fileLoc = fileLoc
            urllib.request.urlretrieve(downloadInfo[0], fileLoc )
            terminalColor.printGreenString("DOWNLOAD FINISHED")
            print("File Saved To: " + fileLoc)
        else:
            terminalColor.printRedString("DOWNLOAD CANCELED")

def readFileList():
    with open(os.path.expanduser('~') + "/HardwareDonations/Settings/DownloadList", 'r') as myfile:
        data=myfile.read()
    obj = json.loads(data)

    typesOfDownload = ["Legal", "PDFs", "Photos", "Wallpapers"]
    categorySelection = 0
    while ( categorySelection < 1 ) or (categorySelection  > ( len(typesOfDownload) + 1 ) ):
        print("\nWhat category do you want to browse for downloads?")
        for i in range (len(typesOfDownload)):
            terminalColor.printBlueString( str(i+1) + ". " + typesOfDownload[i])
        terminalColor.printBlueString( str(len(typesOfDownload) + 1) + ". Cancel" )
        try:
            categorySelection = int(input())
            if ( categorySelection > 0 ) and (categorySelection  <= ( len(typesOfDownload) ) ):
                chooseFileToDownload( obj, typesOfDownload[categorySelection - 1])
                categorySelection = 0
            elif( categorySelection == ( len(typesOfDownload) + 1 ) ):
                return
        except:
            intDecision = 0
            terminalColor.printRedString("Invalid Input")

def chooseFileToDownload( obj, typeOfDownload):
    intDecision = 0
    terminateLoop = False
    urlToDownload = "none"
    nameToDownload = "none"
    extensionToDownload = "none"
    categoryToDownload = "none"
    while ( ( (intDecision < 1) or (intDecision > len(downloadName) + 1 ) ) or (terminateLoop == False) ):
        print("\n")
        downloadURLs = []
        downloadName = []
        downloadExtension = []
        downloadCategory = []
        for downloadable in obj[typeOfDownload]:
            downloadURLs.append(str(downloadable["url"]))
            downloadName.append(str(downloadable["name"]))
            downloadExtension.append(str(downloadable["fileExtention"]))
            downloadCategory.append( typeOfDownload )
            terminalColor.printBlueString( str(len(downloadURLs)) + ". " + downloadable["name"] )
            print("     Description: " + downloadable["description"] )
            print("     Size: " + downloadable["size"] )
            print("     File Extension: " + downloadable["fileExtention"] )
        terminalColor.printBlueString( str( len(downloadName) + 1 ) + ". Cancel" )

        try:
            print("Which file do you want to download?")
            intDecision = int(input())
            if ( (intDecision < 1) or (intDecision > ( len(downloadURLs) + 1 ) ) ):
                terminalColor.printRedString("Invalid Input")
            elif (intDecision == ( len(downloadName) + 1 ) ):
                terminateLoop = True
            else:
                print("\nDownloading URL: " + downloadURLs[intDecision - 1])
                terminateLoop = True
                urlToDownload = downloadURLs[intDecision - 1]
                nameToDownload = downloadName[intDecision - 1]
                extensionToDownload = downloadExtension[intDecision - 1]
                categoryToDownload = downloadCategory[intDecision - 1]
                chooseFolderToSaveFile( [urlToDownload, nameToDownload, extensionToDownload, categoryToDownload] )
        except:
            intDecision = 0
            terminalColor.printRedString("Invalid Input")
    return
