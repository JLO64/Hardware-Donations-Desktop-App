import urllib.request, os, sys, json
import terminalColor, fileFunctions

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
    print("usd: " + str(obj['name']))