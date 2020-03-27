import settingsJson, terminalColor
import sys, os, urllib.request, boto3
try:
    from tkinter import *
    from tkinter import filedialog
except:
    settingsJson.guiMode = False
    pass

def checkForDirectory(programPath): #checks for "programPath" directory and creates it if not found
    if not os.path.exists(programPath):
        os.makedirs(programPath)
    return programPath

def checkForFile(filePath): #checks for "filePath" file and returns boolean
    if os.path.exists(filePath):
        return True
    else: return False

def internet_on():
    for timeout in [1,5,10,15]:
        try:
            response=urllib.request.urlopen('http://google.com',timeout=timeout)
            return True
        except: pass
    return False

def deleteFile(fileLoc):
    os.remove(fileLoc)

def chooseFolderToSaveFile( downloadInfo ):
    if(downloadInfo[1] == "none" ):
        return
    else:
        fileLoc = ""
        if( settingsJson.guiMode == True ):
            root = Tk()
            root.withdraw()
            options = {} #https://www.programcreek.com/python/example/9924/tkFileDialog.asksaveasfilename
            
            if( downloadInfo[2] == ".txt" ):
                options['filetypes'] = [('text files', '.txt')]
            elif( downloadInfo[2] == ".pdf" ):
                options['filetypes'] = [('pdf files', '.pdf')]
            elif( downloadInfo[2] == ".zip" ):
                options['filetypes'] = [('zip files', '.zip')]
            elif( downloadInfo[2] == ".png" ):
                options['filetypes'] = [('png files', '.png')]
            elif( downloadInfo[2] == "unknown" ):
                if ".png" in downloadInfo[0].lower():
                    options['filetypes'] = [('png files', '.png')]
                    downloadInfo[2] = ".png"
                elif ".jpg" in downloadInfo[0].lower():
                    options['filetypes'] = [('jpg files', '.jpg')]
                    downloadInfo[2] = ".jpg"
                elif ".jpeg" in downloadInfo[0].lower():
                    options['filetypes'] = [('jpeg files', '.jpeg')]
                    downloadInfo[2] = ".jpeg"

            if( downloadInfo[3] == "PDFs" ):
                options['initialdir'] = checkForDirectory(os.path.expanduser('~') + "/HardwareDonations/PDF_Files")
            elif( downloadInfo[3] == "Legal" ):
                options['initialdir'] = checkForDirectory(os.path.expanduser('~') + "/HardwareDonations/Legal_Files")
            elif( downloadInfo[3] == "Photos" ):
                options['initialdir'] = checkForDirectory(os.path.expanduser('~') + "/HardwareDonations/Photos")
            elif( downloadInfo[3] == "Wallpapers" ):
                options['initialdir'] = checkForDirectory(os.path.expanduser('~') + "/HardwareDonations/Wallpapers")
            elif( downloadInfo[3] == "Labels" ):
                options['initialdir'] = checkForDirectory(os.path.expanduser('~') + "/HardwareDonations/Labels")
            elif( downloadInfo[3] == "Unit Photos" ):
                options['initialdir'] = checkForDirectory(os.path.expanduser('~') + "/HardwareDonations/Unit_Photos")
                
            options['title'] = "Download As"
            options['initialfile'] = downloadInfo[1] + downloadInfo[2]
            
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
            def _progress(count, block_size, total_size):
                if ( float(count * block_size) / float(total_size) < 1.0):
                    sys.stdout.write(
                        '\rDownloading %.2f%%' % (float(count * block_size) / float(total_size) * 100.0))
                    sys.stdout.flush()
            urllib.request.urlretrieve(downloadInfo[0], fileLoc, reporthook=_progress)
            terminalColor.printGreenString("\nDOWNLOAD FINISHED")
            print("File Saved To: " + fileLoc)
        else:
            terminalColor.printRedString("DOWNLOAD CANCELED")

def uploadToS3(unitID, filename, filepath):
    try:
        print("Uploading to S3")
        itemType = unitID.split("-")[0]
        S3 = boto3.client(
            's3',
            region_name='us-west-1',
            aws_access_key_id=settingsJson.aws_access_key_id,
            aws_secret_access_key=settingsJson.aws_secret_access_key
        )
        UPLOAD_FILELOCATION = "Unit_Photos/" + itemType + "_Units/" + unitID + "/" + filename
        BUCKET_NAME = 'hardware-donations-database-gamma'
        S3.upload_file(filepath, BUCKET_NAME, UPLOAD_FILELOCATION)
        return "https://hardware-donations-database-gamma.s3-us-west-1.amazonaws.com/" + UPLOAD_FILELOCATION
    except: return "false"