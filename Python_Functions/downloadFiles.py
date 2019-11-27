import urllib.request, os, sys, json
import terminalColor, fileFunctions
import array as arr

def downloadFilesMain():
    downloadFilesList()
    readFileList()

def downloadFilesList():
    fileFunctions.checkForDirectory( os.path.expanduser('~') + "/HardwareDonations/Download_Links" )

    print("Downloading list of files")
    url = "https://hardware-donations-database-gamma.s3-us-west-1.amazonaws.com/Misc_Items/DownloadList.txt"
    urllib.request.urlretrieve(url, os.path.expanduser('~') + "/HardwareDonations/Download_Links/DownloadList.txt" )
    terminalColor.printGreenString("Download Finished")

def readFileList():
    with open(os.path.expanduser('~') + "/HardwareDonations/Download_Links/DownloadList.txt", 'r') as myfile:
        data=myfile.read()
    obj = json.loads(data)

    intDecision = 0
    terminateLoop = False
    while ( ( (intDecision < 1) or (intDecision > len(downloadURLs)) ) or (terminateLoop == False) ):
        
        downloadURLs = []
        for downloadable in obj["Legal"]:
            downloadURLs.append(str(downloadable["url"]))
            terminalColor.printBlueString( str(len(downloadURLs)) + ". [Legal]" + downloadable["name"] )
            print("     Description: " + downloadable["description"] )
            print("     Size: " + downloadable["size"] )
        for downloadable in obj["PDFs"]:
            downloadURLs.append(str(downloadable["url"]))
            terminalColor.printBlueString( str(len(downloadURLs)) + ". [PDF]" + downloadable["name"] )
            print("     Description: " + downloadable["description"] )
            print("     Size: " + downloadable["size"] )
        terminalColor.printBlueString( str(len(downloadURLs) + 1 ) + ". Exit" )

        try:
            print("Which file do you want to download?")
            intDecision = int(input())
            if ( (intDecision < 1) or (intDecision > ( len(downloadURLs) + 1 ) ) ):
                terminalColor.printRedString("Invalid Input")
            elif (intDecision == ( len(downloadURLs) ) ):
                terminateLoop = True
            else:
                print("Downloading URL: " + downloadURLs[intDecision - 1])
                terminateLoop = True
        except:
            intDecision = 0
            terminalColor.printRedString("Invalid Input")
    