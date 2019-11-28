import urllib.request, os, sys, json
import terminalColor, fileFunctions
import array as arr
from tkinter import filedialog
from tkinter import *

def downloadFilesMain():
    downloadFilesList()
    chooseFolderToSaveFile( readFileList() )

def downloadFilesList():
    fileFunctions.checkForDirectory( os.path.expanduser('~') + "/HardwareDonations/Download_Links" )

    print("Downloading list of files")
    url = "https://hardware-donations-database-gamma.s3-us-west-1.amazonaws.com/Misc_Items/DownloadList.txt"
    urllib.request.urlretrieve(url, os.path.expanduser('~') + "/HardwareDonations/Download_Links/DownloadList.txt" )
    terminalColor.printGreenString("Download Finished")

def chooseFolderToSaveFile( downloadInfo ):
    if(downloadInfo[1] == "none" ):
        return
    else:
        root = Tk()
        root.withdraw()
        options = {} #https://www.programcreek.com/python/example/9924/tkFileDialog.asksaveasfilename
        options['title'] = "Save As"
        options['initialfile'] = downloadInfo[1]
        fileLoc = filedialog.asksaveasfile(mode='w', **options)
        if (fileLoc == None):
            terminalColor.printRedString("DOWNLOAD CANCELED")
        #folder_selected = filedialog.askdirectory()
        #urllib.request.urlretrieve(downloadInfo[0], folder_selected + "/testDownload.txt" )

def readFileList():
    with open(os.path.expanduser('~') + "/HardwareDonations/Download_Links/DownloadList.txt", 'r') as myfile:
        data=myfile.read()
    obj = json.loads(data)

    intDecision = 0
    terminateLoop = False
    urlToDownload = "none"
    nameToDownload = "none"
    while ( ( (intDecision < 1) or (intDecision > len(downloadURLs) + 1 ) ) or (terminateLoop == False) ):
        
        downloadURLs = []
        downloadName = []
        for downloadable in obj["Legal"]:
            downloadURLs.append(str(downloadable["url"]))
            downloadName.append(str(downloadable["name"]))
            terminalColor.printBlueString( str(len(downloadURLs)) + ". [Legal]" + downloadable["name"] )
            print("     Description: " + downloadable["description"] )
            print("     Size: " + downloadable["size"] )
        for downloadable in obj["PDFs"]:
            downloadURLs.append(str(downloadable["url"]))
            downloadName.append(str(downloadable["name"]))
            terminalColor.printBlueString( str(len(downloadURLs)) + ". [PDF]" + downloadable["name"] )
            print("     Description: " + downloadable["description"] )
            print("     Size: " + downloadable["size"] )
        terminalColor.printBlueString( str(len(downloadURLs) + 1 ) + ". Cancel" )

        try:
            print("Which file do you want to download?")
            intDecision = int(input())
            if ( (intDecision < 1) or (intDecision > ( len(downloadURLs) + 1 ) ) ):
                terminalColor.printRedString("Invalid Input")
            elif (intDecision == ( len(downloadURLs) + 1 ) ):
                terminateLoop = True
            else:
                print("Downloading URL: " + downloadURLs[intDecision - 1])
                terminateLoop = True
                urlToDownload = downloadURLs[intDecision - 1]
                nameToDownload = downloadName[intDecision - 1]
        except:
            intDecision = 0
            terminalColor.printRedString("Invalid Input")
    return [urlToDownload, nameToDownload]