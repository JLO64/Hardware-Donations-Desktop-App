import urllib.request, os, sys
import terminalColor, fileFunctions

def downloadFilesMain():
    downloadFilesList()

def downloadFilesList():
    fileFunctions.checkForDirectory( os.path.expanduser('~') + "/HardwareDonations/Download_Links" )

    print("Downloading list of files")
    url = "https://hardware-donations-database-gamma.s3-us-west-1.amazonaws.com/Misc_Items/Hardware_Donations_Account_EULA.txt"
    urllib.request.urlretrieve(url, os.path.expanduser('~') + "/HardwareDonations/Download_Links/downloadsList.txt" )
    terminalColor.printGreenString("Download Finished")
