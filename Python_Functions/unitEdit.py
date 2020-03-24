import boto3, json, getpass, os, click
import terminalColor, settingsJson, fileFunctions, unitEdit, browseDatabase
import array as arr
from pyautogui import typewrite
try: import readline
except: settingsJson.externalEditor = True

lambda_client = boto3.client('lambda')

def unitEditOptions(responseJson, unitID): #unit options user is given
    intDecision = 0
    listOfOptions =[". Edit Entry",". Download Unit Photos", ". Download Unit Label", ". Download Unit PDF", ". Delete Unit", ". Exit"]
    while ( (intDecision < 1 ) or (intDecision > len(listOfOptions)) ):
        try:
            printUnitInfo(responseJson, unitID)
            print("\nWhat do you want to do with this unit?")
            for i in range( len(listOfOptions) ): terminalColor.printBlueString( str(i+1) + listOfOptions[i] )
            intDecision = int(input())
            if ( (intDecision < 1) or (intDecision > len(listOfOptions)) ): terminalColor.printRedString("Invalid Input")
            elif ( listOfOptions[intDecision-1] == ". Exit"): break
            elif ( listOfOptions[intDecision-1] == ". Edit Entry"):
                intDecision = 0
                responseJson = unitEditEntry(responseJson, "Editing Existing Unit")
            elif ( listOfOptions[intDecision-1] == ". Delete Unit"):
                if deleteUnit(unitID): terminalColor.printGreenString("Unit Deleted")
                else: intDecision = 0
            elif ( listOfOptions[intDecision-1] == ". Download Unit Photos"):
                intDecision = 0
                try:
                    unitInfo = responseJson["unitInfo"]
                    if unitInfo["Photo_URL"] == "https://hardware-donations-database-gamma.s3-us-west-1.amazonaws.com/Misc_Items/noPhotoFound.png":
                        terminalColor.printRedString("No unit photos uploaded")
                    else: downloadUnitPhoto(responseJson)
                except:
                    terminalColor.printRedString("Unable to download unit photos")
            elif ( listOfOptions[intDecision-1] == ". Download Unit Label"):
                intDecision = 0
                try:
                    downloadUnitLabel(unitID)
                except:
                    try:
                        createNewUnitLabel(unitID)
                        downloadUnitLabel(unitID)
                    except:
                        terminalColor.printRedString("Unable to download unit label")
            elif ( listOfOptions[intDecision-1] == ". Download Unit PDF"):
                intDecision = 0
                try:
                    downloadUnitPDF(unitID)
                except:
                    try:
                        createNewUnitPDF(unitID, responseJson)
                        downloadUnitPDF(unitID)
                    except:
                        terminalColor.printRedString("Unable to download unit PDF")
        except:
            intDecision = 0
            terminalColor.printRedString("Invalid Input")

def unitEditEntry(responseJson, typeOfEditing): #User selects what category they want to edit
    unitInfo = responseJson["unitInfo"]
    intDecision = 0
    listOfOptions = [". Location", ". Status", ". User ID",". Manufacturer",". Model",". ARK-OS Version", ". Original Operating System", ". CPU Model", ". CPU GHz",". CPU Threads",". CPU Architecture",". RAM GB",". RAM Slots",". RAM Type", ". HDD GB", ". HDD Port",". HDD Speed",". USB Ports",". Audio Ports",". Display Ports",". External Disk Drives",". Networking",". Other Ports", ". Comments", ". Exit", ". Save and Exit"]
    listOfCategories = ["Location", "Status", "UserID", "Manufacturer", "Model", "ARK-OS_Version", "Operating System", "CPU Type", "CPU GHz", "CPU Threads","CPU Architecture","RAM","RAM Slots","RAM Type", "HDD", "HDD Port","HDD Speed","USB Ports","Audio Ports","Display Ports","Disk Drive","Networking","Ports", "Comments"]
    stuffToUpdate = {}
    while ( (intDecision < 1 ) or (intDecision > len(listOfOptions)) ):
        try:
            print("\nWhat section do you want to edit?")
            for i in range( len(listOfOptions) - 1):
                if ( len(listOfCategories) > i and listOfCategories[i] in stuffToUpdate ): terminalColor.printGreenRegString( str(i+1) + listOfOptions[i] )
                else: terminalColor.printBlueString( str(i+1) + listOfOptions[i] )
            if len(stuffToUpdate) > 0: terminalColor.printBlueString( str(len(listOfOptions)) + listOfOptions[len(listOfOptions) - 1] ) #Prints "Save and Exit"
            intDecision = int(input())
            if ( (intDecision) == 20207864):
                for i in listOfCategories:
                    stuffToUpdate[i] = "[REDACTED]"
            elif ( (intDecision < 1) or (intDecision > len(listOfOptions)) ): terminalColor.printRedString("Invalid Input")
            elif ( listOfOptions[intDecision-1] == ". Exit" ):
                try: testVariable = responseJson["Unit_ID"]
                except: responseJson["Unit_ID"] = "bad"
                return responseJson
            elif ( listOfOptions[intDecision-1] == ". Save and Exit" ) and len(stuffToUpdate) > 0:
                if typeOfEditing == "Editing Existing Unit":
                    if verifyUploadData(stuffToUpdate): return uploadUnitUpdate(stuffToUpdate, unitInfo["Unit_ID"])
                    else:
                        intDecision = 0
                elif typeOfEditing == "Creating New Unit":
                    if len(stuffToUpdate) > 23:
                        if verifyUploadData(stuffToUpdate): 
                            stuffToUpdate["Unit_ID"] = "OkToUpload"
                            return stuffToUpdate
                        else:
                            intDecision = 0
                    else:
                        intDecision = 0
                        terminalColor.printRedString("Please fill out all fields before creating a new unit")
            elif ( listOfOptions[intDecision-1] == ". Comments"):
                intDecision = 0
                try: oldComments = stuffToUpdate["Comments"]
                except: oldComments = unitInfo["Comments"]
                newComments = click.edit(oldComments)
                stuffToUpdate["Comments"] = newComments
            elif checkIfCategoryHasLists(listOfCategories[intDecision-1]):
                category = listOfCategories[intDecision-1]
                intDecision = 0
                originalData = unitInfo[category]
                try: oldData = stuffToUpdate[category]
                except: oldData = unitInfo[category]
                if category == "RAM Type": newData = changeRAMType(originalData, oldData)
                elif category == "CPU Architecture": newData = changeCPUArchitecture(originalData, oldData)
                elif category == "ARK-OS_Version": newData = changeARKOSVersion(originalData, oldData)
                elif category == "Location": newData = changeUnitLocation(originalData, oldData)
                if newData == originalData and category in stuffToUpdate: del stuffToUpdate[category]
                elif not newData == originalData: stuffToUpdate[category] = newData
            else:
                stuffToUpdate = editTextEntry(stuffToUpdate, unitInfo, listOfCategories[intDecision-1])
                intDecision = 0
        except:
            intDecision = 0
            terminalColor.printRedString("Invalid Input")

def uploadUnitUpdate(stuffToUpdate, unitID): #Connects to AWS lambda to update unit data
    payload = dict(key1=settingsJson.key1, key2=settingsJson.key2, key3=settingsJson.key3, type="unit_update", unitID=unitID, updateInfo=stuffToUpdate)
    response = lambda_client.invoke(
        FunctionName='arn:aws:lambda:us-west-1:105369739187:function:HDPasswordCheck',
        InvocationType='RequestResponse',
        Payload=json.dumps(payload),
    )
    passTest=json.loads(response['Payload'].read())
    responseJson=passTest["unitInfo"]
    return passTest

def printUnitInfo(responseJson, unitID): #Prints out data on units
    try:
        unitInfo = responseJson["unitInfo"]
        print("\nInfo Page For " + unitID )
        terminalColor.printCyanString(" " + unitID )
        print( terminalColor.generateYellowString( "  Unit Category: " ) + unitInfo["Category"])
        print( terminalColor.generateYellowString( "  Unit Number: " ) + unitID.split("-",1)[1] )
        print( terminalColor.generateYellowString( "  Location: " ) + unitInfo["Location"])
        print( terminalColor.generateYellowString( "  Status: " ) + unitInfo["Status"])
        print( terminalColor.generateYellowString( "  User ID: " ) + unitInfo["UserID"])
        terminalColor.printCyanString( " System Info")
        print( terminalColor.generateYellowString( "  Manufacturer: " ) + unitInfo["Manufacturer"])
        print( terminalColor.generateYellowString( "  Model: " ) + unitInfo["Model"])
        print( terminalColor.generateYellowString( "  ARK-OS Version: " ) + unitInfo["ARK-OS_Version"])
        print( terminalColor.generateYellowString( "  Original Operating System: " ) + unitInfo["Operating System"])
        terminalColor.printCyanString(" CPU")
        print( terminalColor.generateYellowString( "  CPU Model: " ) + unitInfo["CPU Type"])
        print( terminalColor.generateYellowString( "  CPU GHz: " ) + unitInfo["CPU GHz"])
        print( terminalColor.generateYellowString( "  CPU Threads: " ) + unitInfo["CPU Threads"])
        print( terminalColor.generateYellowString( "  CPU Architecture: " ) + unitInfo["CPU Architecture"])
        terminalColor.printCyanString( " RAM")
        print( terminalColor.generateYellowString( "  RAM GB: " ) + unitInfo["RAM"])
        print( terminalColor.generateYellowString( "  RAM Slots: " ) + unitInfo["RAM Slots"])
        print( terminalColor.generateYellowString( "  RAM Type: " ) + unitInfo["RAM Type"])
        terminalColor.printCyanString( " HDD")
        print( terminalColor.generateYellowString( "  HDD Size: " ) + unitInfo["HDD"])
        print( terminalColor.generateYellowString( "  HDD Port: " ) + unitInfo["HDD Port"])
        print( terminalColor.generateYellowString( "  HDD Speed: " ) + unitInfo["HDD Speed"])
        terminalColor.printCyanString( " Ports")
        print( terminalColor.generateYellowString( "  USB Ports: " ) + unitInfo["USB Ports"])
        print( terminalColor.generateYellowString( "  Audio Ports: " ) + unitInfo["Audio Ports"])
        print( terminalColor.generateYellowString( "  Display Ports: " ) + unitInfo["Display Ports"])
        print( terminalColor.generateYellowString( "  External Disk Drives: " ) + unitInfo["Disk Drive"])
        print( terminalColor.generateYellowString( "  Networking: " ) + unitInfo["Networking"])
        print( terminalColor.generateYellowString( "  Other Ports: " ) + unitInfo["Ports"])
        print( terminalColor.generateCyanString( " Comments: ") + unitInfo["Comments"])
    except:
        terminalColor.printRedString("Unable to print all data")

def downloadUnitLabel(unitID): #downloads unit label from AWS S3
    awsURL = "https://hardware-donations-database-gamma.s3-us-west-1.amazonaws.com/Unit_Photos/"
    unitType = unitID.split("-",1)[0]
    unitLabelUrl = awsURL + unitType + "_Units/" + unitID + "/" + unitID + "_QR_Label.png"
    fileFunctions.chooseFolderToSaveFile( [unitLabelUrl, unitID + " Label", ".png", "Labels"] )

def downloadUnitPhoto(responseJson): #downloads unit photo from AWS S3
    unitInfo = responseJson["unitInfo"]
    fileFunctions.chooseFolderToSaveFile( [unitInfo["Photo_URL"], unitInfo["Unit_ID"] + "_Photo", "unknown", "Unit Photos"] )

def downloadUnitPDF(unitID): #downloads unit pdf from AWS S3
    awsURL = "https://hardware-donations-database-gamma.s3-us-west-1.amazonaws.com/Unit_Photos/"
    unitType = unitID.split("-",1)[0]
    unitPDFUrl = awsURL + unitType + "_Units/" + unitID + "/" + unitID + "_Info_Page.pdf"
    fileFunctions.chooseFolderToSaveFile( [unitPDFUrl, unitID + " Info Page", ".pdf", "PDFs"] )

def createNewUnitLabel(unitID): #connects to AWS Lambda to generate a label for the unit
    itemType = unitType = unitID.split("-",1)[0]
    itemNumber = unitType = unitID.split("-",1)[1]
    payload = dict(itemType=itemType, itemNumber=itemNumber)
    response = lambda_client.invoke(
        FunctionName='arn:aws:lambda:us-west-1:105369739187:function:HDLabelGenerator',
        InvocationType='RequestResponse',
        Payload=json.dumps(payload),
    )
    passTest=json.loads(response['Payload'].read())
    labelURL=passTest["qrLabelURL"]

def createNewUnitPDF(unitID, unitInfo): #connects to AWS Lambda to generate a label for the unit
    payload = dict(unitID=unitID, unitInfo=unitInfo)
    response = lambda_client.invoke(
        FunctionName='arn:aws:lambda:us-west-1:105369739187:function:Hardware-Donations-PDF-Generator',
        InvocationType='RequestResponse',
        Payload=json.dumps(payload),
    )

def changeUnitLocation(original, current): #Selects version of ARK-OS
    unitLocations = ["Unknown","Donated","Site 1(Bosco Tech)","Site 2(Roosevelt)","Site 3(ELAC)", "Cancel"]
    intDecision = 0
    while ( (intDecision < 1 ) or (intDecision > len(unitLocations)) ):
        try:
            print("\nWhere is this unit located?")
            print("Original Location Version Data: " + original)
            print("Current Location Version Data: " + current)
            for i in range( len(unitLocations) ): terminalColor.printBlueString( str(i+1) + ". " + unitLocations[i])
            intDecision = int(input())
            if ( (intDecision < 1) or (intDecision > len(unitLocations)) ): terminalColor.printRedString("Invalid Input")
            elif unitLocations[intDecision -1] == "Cancel": return current
            else: return unitLocations[intDecision - 1]
        except:
            intDecision = 0
            terminalColor.printRedString("Invalid Input")

def changeARKOSVersion(original, current): #Selects version of ARK-OS
    arkosVersions = ["Unknown","None","Experimental","v1.0.6","v1.1.2","v1.2.1","v2.0.1 \"Bosco\"","v2.1.0 \"Bosco Tech\"", "Cancel"]
    intDecision = 0
    while ( (intDecision < 1 ) or (intDecision > len(arkosVersions)) ):
        try:
            print("\nWhat version of ARK-OS does this unit have installed?")
            print("Original ARK-OS Version Data: " + original)
            print("Current ARK-OS Version Data: " + current)
            for i in range( len(arkosVersions) ): terminalColor.printBlueString( str(i+1) + ". " + arkosVersions[i])
            intDecision = int(input())
            if ( (intDecision < 1) or (intDecision > len(arkosVersions)) ): terminalColor.printRedString("Invalid Input")
            elif arkosVersions[intDecision -1] == "Cancel": return current
            else: return arkosVersions[intDecision - 1]
        except:
            intDecision = 0
            terminalColor.printRedString("Invalid Input")

def changeCPUArchitecture(original, current): #Selects CPU Arch.
    cpuArchitectures = ["Unknown","64-Bit","32-Bit","PowerPC","Cancel"]
    intDecision = 0
    while ( (intDecision < 1 ) or (intDecision > len(cpuArchitectures)) ):
        try:
            print("\nWhat CPU Architecture does this unit have?")
            print("Original CPU Architecture Data: " + original)
            print("Current CPU Architecture Data: " + current)
            for i in range( len(cpuArchitectures) ): terminalColor.printBlueString( str(i+1) + ". " + cpuArchitectures[i])
            intDecision = int(input())
            if ( (intDecision < 1) or (intDecision > len(cpuArchitectures)) ): terminalColor.printRedString("Invalid Input")
            elif cpuArchitectures[intDecision -1] == "Cancel": return current
            else: return cpuArchitectures[intDecision -1]
        except:
            intDecision = 0
            terminalColor.printRedString("Invalid Input")

def changeRAMType(original, current): #Selects type of RAM
    ramType = ["Unknown","Other","DDR RAM","DDR2 RAM","DDR3 RAM","DDR4 RAM","DDR SDRAM","DDR2 SDRAM","DDR3 SDRAM","DDR4 SDRAM","Cancel"]
    intDecision = 0
    while ( (intDecision < 1 ) or (intDecision > len(ramType)) ):
        try:
            print("\nWhat type of RAM does this unit have?")
            print("Original RAM Type Data: " + original)
            print("Current RAM Type Data: " + current)
            for i in range( len(ramType) ): terminalColor.printBlueString( str(i+1) + ". " + ramType[i])
            intDecision = int(input())
            if ( (intDecision < 1) or (intDecision > len(ramType)) ): terminalColor.printRedString("Invalid Input")
            elif ramType[intDecision -1] == "Cancel": return current
            else: return ramType[intDecision - 1]
        except:
            intDecision = 0
            terminalColor.printRedString("Invalid Input")

def editTextEntry(stuffToUpdate, unitInfo, category): #code to edit data in a category
    copyOfStuffToUpdate = stuffToUpdate.copy()
    originalData = unitInfo[category]
    try: oldData = copyOfStuffToUpdate[category]
    except: oldData = unitInfo[category]
    print("Original " + category + " Data: " + originalData)
    newData = methodOfEditingString(category +": " ,oldData)
    while len(newData) < 2 or len(newData) > 70:
        terminalColor.printRedString("The data you entered is too long or short")
        newData = methodOfEditingString(category +": " ,oldData)
    if newData == originalData and category in copyOfStuffToUpdate: del copyOfStuffToUpdate[category]
    elif not newData == originalData: copyOfStuffToUpdate[category] = newData
    return copyOfStuffToUpdate

def deleteUnit(unitID): #connects to AWS Lambda to delete a unit
    try:
        payload = dict(key1=settingsJson.key1, key2=settingsJson.key2, key3=settingsJson.key3, type="unit_delete", unitID=unitID)
        response = lambda_client.invoke(
            FunctionName='arn:aws:lambda:us-west-1:105369739187:function:HDPasswordCheck',
            InvocationType='RequestResponse',
            Payload=json.dumps(payload),
        )
        responseJSON=json.loads(response['Payload'].read())
        if not responseJSON["result"]: terminalColor.printRedString("Failed to delete unit: " + responseJSON["reason"])
        return responseJSON["result"]
    except:
        return False

def checkIfCategoryHasLists(category):
    categoryWithLists = ["RAM Type","CPU Architecture","ARK-OS_Version","Location"]
    if category in categoryWithLists: return True
    return False

def verifyUploadData(jsonToUpload):
    uploadDataOk = False
    while not uploadDataOk:
        for x in jsonToUpload: print(terminalColor.generateYellowString(x) + ": " + jsonToUpload[x] )
        print("\nDo you want to want to upload these changes?[Yes/No]")
        strDecision = input()
        if strDecision.lower() == "yes" or strDecision.lower() == "y": return True
        elif strDecision.lower() == "no" or strDecision.lower() == "n": return False
        else: terminalColor.printRedString("Invalid Input")                        

def methodOfEditingString(prompt, dataToEdit):
    if settingsJson.externalEditor: return click.edit(dataToEdit).replace("\n", "")
    else: return rlinput(prompt ,dataToEdit)

def rlinput(prompt, prefill=''): #code for input with text prefilled in
   readline.set_startup_hook(lambda: readline.insert_text(prefill))
   try:
      return input(prompt)
   finally:
      readline.set_startup_hook()