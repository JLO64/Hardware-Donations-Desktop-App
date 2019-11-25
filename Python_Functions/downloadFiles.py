import urllib.request
import terminalColor

def downloadFilesMain( mainFileDir ):
    downloadFilesList( mainFileDir )

def downloadFilesList( mainFileDir ):
    print("Downloading list of files")
    url = "https://hardware-donations-database-gamma.s3-us-west-1.amazonaws.com/Misc_Items/Hardware_Donations_Account_EULA.txt"
    urllib.request.urlretrieve(url, mainFileDir + "/Download_Links/downloadsList.txt" )
    terminalColor.printGreenString("Download Finished")
