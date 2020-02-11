import boto3, json, getpass, os, click
import terminalColor, settingsJson, fileFunctions, unitEdit
import array as arr

lambda_client = boto3.client('lambda')

def unitEditOptions(responseJson, unitID):
    intDecision = 0
    listOfOptions =[". Edit Entry", ". Download Unit Label", ". Exit"]
    while ( (intDecision < 1 ) or (intDecision > len(listOfOptions)) ):
        try:
            printUnitInfo(responseJson, unitID)
            print("\nWhat do you want to do with this unit?")
            for i in range( len(listOfOptions) ): terminalColor.printBlueString( str(i+1) + listOfOptions[i] )
            intDecision = int(input())
            if ( (intDecision < 1) or (intDecision > len(listOfOptions)) ): terminalColor.printRedString("Invalid Input")
            elif ( listOfOptions[intDecision-1] == ". Exit"): break
            elif ( listOfOptions[intDecision-1] == ". Edit Entry"): unitEditEntry(responseJson)
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
        except:
            intDecision = 0
            terminalColor.printRedString("Invalid Input")

def unitEditEntry(responseJson):
    unitInfo = responseJson["unitInfo"]
    intDecision = 0
    listOfOptions =[". Location", ". Status", ". User ID",". Manufacturer",". Model",". ARK-OS Version", ". Original Operating System", ". CPU Model", ". CPU GHz",". CPU Threads",". CPU Architecture",". RAM GB",". RAM Slots",". RAM Type", ". HDD GB", ". Comments", ". Exit", ". Save and Exit"]
    stuffToUpdate = {}
    changesMade = False
    while ( (intDecision < 1 ) or (intDecision > len(listOfOptions)) ):
        try:
            print("\nWhat section do you want to edit?")
            for i in range( len(listOfOptions) - 1): terminalColor.printBlueString( str(i+1) + listOfOptions[i] )
            if changesMade: terminalColor.printBlueString( str(len(listOfOptions)) + listOfOptions[len(listOfOptions) - 1] )
            intDecision = int(input())
            if ( (intDecision < 1) or (intDecision > len(listOfOptions)) ): terminalColor.printRedString("Invalid Input")
            elif ( listOfOptions[intDecision-1] == ". Exit" ):
                unitEditOptions(responseJson, unitInfo["Unit_ID"])
                break
            elif ( listOfOptions[intDecision-1] == ". Save and Exit" ) and changesMade:
                for x in stuffToUpdate:
                    data = stuffToUpdate[x]
                    print(terminalColor.generateYellowString(x) + ": " + data )
                print("\nDo you want to want to upload these changes?[Yes/No]")
                strDecision = input()
                if strDecision.lower() == "yes" or strDecision.lower() == "y":
                    uploadUnitUpdate(stuffToUpdate, unitInfo["Unit_ID"])
                    break
                else:
                    intDecision = 0
            elif ( listOfOptions[intDecision-1] == ". Comments"):
                intDecision = 0
                try: oldComments = stuffToUpdate["Comments"]
                except: oldComments = unitInfo["Comments"]
                newComments = click.edit(oldComments)
                stuffToUpdate["Comments"] = newComments
                if oldComments != newComments: changesMade = True
            elif ( listOfOptions[intDecision-1] == ". Location"):
                intDecision = 0
                try: oldLocation = stuffToUpdate["Location"]
                except: oldLocation = unitInfo["Location"]
                newLocation = changeUnitLocation()
                stuffToUpdate["Location"] = newLocation
                if oldLocation != newLocation: changesMade = True
            elif ( listOfOptions[intDecision-1] == ". Status"):
                intDecision = 0
                arrayOfChanges = editTextEntry(stuffToUpdate, unitInfo, "Status")
                stuffToUpdate = arrayOfChanges["stuffToUpdate"]
                changesMade = arrayOfChanges["changesMade"]
            elif ( listOfOptions[intDecision-1] == ". User ID"):
                intDecision = 0
                arrayOfChanges = editTextEntry(stuffToUpdate, unitInfo, "UserID")
                stuffToUpdate = arrayOfChanges["stuffToUpdate"]
                changesMade = arrayOfChanges["changesMade"]
            elif ( listOfOptions[intDecision-1] == ". Manufacturer"):
                intDecision = 0
                arrayOfChanges = editTextEntry(stuffToUpdate, unitInfo, "Manufacturer")
                stuffToUpdate = arrayOfChanges["stuffToUpdate"]
                changesMade = arrayOfChanges["changesMade"]
            elif ( listOfOptions[intDecision-1] == ". Model"):
                intDecision = 0
                arrayOfChanges = editTextEntry(stuffToUpdate, unitInfo, "Model")
                stuffToUpdate = arrayOfChanges["stuffToUpdate"]
                changesMade = arrayOfChanges["changesMade"]
            elif ( listOfOptions[intDecision-1] == ". ARK-OS Version"):
                intDecision = 0
                originalData = unitInfo["ARK-OS_Version"]
                try: oldData = stuffToUpdate["ARK-OS_Version"]
                except: oldData = unitInfo["ARK-OS_Version"]
                newData = changeARKOSVersion()
                stuffToUpdate["ARK-OS_Version"] = newData
                if originalData == newData: changesMade = False
                elif oldData != newData: changesMade = True
                else: changesMade = False
            elif ( listOfOptions[intDecision-1] == ". Original Operating System"):
                intDecision = 0
                arrayOfChanges = editTextEntry(stuffToUpdate, unitInfo, "Operating System")
                stuffToUpdate = arrayOfChanges["stuffToUpdate"]
                changesMade = arrayOfChanges["changesMade"]
            elif ( listOfOptions[intDecision-1] == ". CPU Model"):
                intDecision = 0
                arrayOfChanges = editTextEntry(stuffToUpdate, unitInfo, "CPU Type")
                stuffToUpdate = arrayOfChanges["stuffToUpdate"]
                changesMade = arrayOfChanges["changesMade"]
            elif ( listOfOptions[intDecision-1] == ". CPU GHz"):
                intDecision = 0
                arrayOfChanges = editTextEntry(stuffToUpdate, unitInfo, "CPU GHz")
                try:
                    stuffToUpdateCopy = arrayOfChanges["stuffToUpdate"]
                    doubleTest = float(stuffToUpdateCopy["CPU GHz"])
                    stuffToUpdate = arrayOfChanges["stuffToUpdate"]
                    changesMade = arrayOfChanges["changesMade"]
                except:
                    terminalColor.printRedString("Invalid Input")
            elif ( listOfOptions[intDecision-1] == ". CPU Threads"):
                intDecision = 0
                arrayOfChanges = editTextEntry(stuffToUpdate, unitInfo, "CPU Threads")
                try:
                    stuffToUpdateCopy = arrayOfChanges["stuffToUpdate"]
                    intTest = int(stuffToUpdateCopy["CPU Threads"])
                    stuffToUpdate = arrayOfChanges["stuffToUpdate"]
                    changesMade = arrayOfChanges["changesMade"]
                except:
                    terminalColor.printRedString("Invalid Input")
            elif ( listOfOptions[intDecision-1] == ". CPU Architecture"):
                intDecision = 0
                originalData = unitInfo["CPU Architecture"]
                try: oldData = stuffToUpdate["CPU Architecture"]
                except: oldData = unitInfo["CPU Architecture"]
                newData = changeCPUArchitecture()
                stuffToUpdate["CPU Architecture"] = newData
                if originalData == newData: changesMade = False
                elif oldData != newData: changesMade = True
                else: changesMade = False
            elif ( listOfOptions[intDecision-1] == ". RAM GB"):
                intDecision = 0
                arrayOfChanges = editTextEntry(stuffToUpdate, unitInfo, "RAM")
                try:
                    stuffToUpdateCopy = arrayOfChanges["stuffToUpdate"]
                    doubleTest = float(stuffToUpdateCopy["RAM"])
                    stuffToUpdate = arrayOfChanges["stuffToUpdate"]
                    changesMade = arrayOfChanges["changesMade"]
                except:
                    terminalColor.printRedString("Invalid Input")
            elif ( listOfOptions[intDecision-1] == ". RAM Slots"):
                intDecision = 0
                arrayOfChanges = editTextEntry(stuffToUpdate, unitInfo, "RAM Slots")
                stuffToUpdate = arrayOfChanges["stuffToUpdate"]
                changesMade = arrayOfChanges["changesMade"]
            elif ( listOfOptions[intDecision-1] == ". RAM Type"):
                intDecision = 0
                originalData = unitInfo["RAM Type"]
                try: oldData = stuffToUpdate["RAM Type"]
                except: oldData = unitInfo["RAM Type"]
                newData = changeRAMType()
                stuffToUpdate["RAM Type"] = newData
                if originalData == newData: changesMade = False
                elif oldData != newData: changesMade = True
                else: changesMade = False
            elif ( listOfOptions[intDecision-1] == ". HDD GB"):
                intDecision = 0
                arrayOfChanges = editTextEntry(stuffToUpdate, unitInfo, "HDD")
                try:
                    stuffToUpdateCopy = arrayOfChanges["stuffToUpdate"]
                    doubleTest = int(stuffToUpdateCopy["HDD"])
                    stuffToUpdate = arrayOfChanges["stuffToUpdate"]
                    changesMade = arrayOfChanges["changesMade"]
                except:
                    terminalColor.printRedString("Invalid Input")
        except:
            intDecision = 0
            terminalColor.printRedString("Invalid Input")

def uploadUnitUpdate(stuffToUpdate, unitID):
    payload = dict(key1=settingsJson.key1, key2=settingsJson.key2, key3=settingsJson.key3, type="unit_update", unitID=unitID, updateInfo=stuffToUpdate)
    response = lambda_client.invoke(
        FunctionName='arn:aws:lambda:us-west-1:105369739187:function:HDPasswordCheck',
        InvocationType='RequestResponse',
        Payload=json.dumps(payload),
    )
    passTest=json.loads(response['Payload'].read())
    responseJson=passTest["unitInfo"]
    unitEditOptions(passTest, responseJson["Unit_ID"])

def printUnitInfo(responseJson, unitID):
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

def downloadUnitLabel(unitID):
    #https://hardware-donations-database-gamma.s3-us-west-1.amazonaws.com/Unit_Photos/HDD_Units/HDD-3/HDD-3_QR_Label.png
    awsURL = "https://hardware-donations-database-gamma.s3-us-west-1.amazonaws.com/Unit_Photos/"
    unitType = unitID.split("-",1)[0]
    unitLabelUrl = awsURL + unitType + "_Units/" + unitID + "/" + unitID + "_QR_Label.png"
    urlToDownload = unitLabelUrl
    nameToDownload = unitID + " Label"
    extensionToDownload = ".png"
    categoryToDownload = "Labels"
    fileFunctions.chooseFolderToSaveFile( [urlToDownload, nameToDownload, extensionToDownload, categoryToDownload] )

def createNewUnitLabel(unitID):
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

def changeUnitLocation():
    unitLocations = ["Unknown","Donated","Site 1(Bosco Tech)","Site 2(Roosevelt)","Site 3(ELAC)"]
    intDecision = 0
    while ( (intDecision < 1 ) or (intDecision > len(unitLocations)) ):
        try:
            print("\nWhere is this unit located?")
            for i in range( len(unitLocations) ): terminalColor.printBlueString( str(i+1) + ". " + unitLocations[i])
            intDecision = int(input())
            if ( (intDecision < 1) or (intDecision > len(unitLocations)) ): terminalColor.printRedString("Invalid Input")
            else: return unitLocations[intDecision - 1]
        except:
            intDecision = 0
            terminalColor.printRedString("Invalid Input")

def changeARKOSVersion():
    arkosVersions = ["Unknown","None","v1.0.6","v1.1.2","v1.2.1","v2.0.1 \"Bosco\"","v2.1.0 \"Bosco Tech\""]
    intDecision = 0
    while ( (intDecision < 1 ) or (intDecision > len(arkosVersions)) ):
        try:
            print("\nWhat version of ARK-OS does this unit have installed?")
            for i in range( len(arkosVersions) ): terminalColor.printBlueString( str(i+1) + ". " + arkosVersions[i])
            intDecision = int(input())
            if ( (intDecision < 1) or (intDecision > len(arkosVersions)) ): terminalColor.printRedString("Invalid Input")
            else: return arkosVersions[intDecision - 1]
        except:
            intDecision = 0
            terminalColor.printRedString("Invalid Input")

def changeCPUArchitecture():
    cpuArchitectures = ["Unknown","64-Bit","32-Bit","PowerPC"]
    intDecision = 0
    while ( (intDecision < 1 ) or (intDecision > len(cpuArchitectures)) ):
        try:
            print("\nWhat CPU architecture does this unit have?")
            for i in range( len(cpuArchitectures) ): terminalColor.printBlueString( str(i+1) + ". " + cpuArchitectures[i])
            intDecision = int(input())
            if ( (intDecision < 1) or (intDecision > len(cpuArchitectures)) ): terminalColor.printRedString("Invalid Input")
            else: return cpuArchitectures[intDecision - 1]
        except:
            intDecision = 0
            terminalColor.printRedString("Invalid Input")

def changeRAMType():
    ramType = ["Unknown","Other","DDR RAM","DDR2 RAM","DDR3 RAM","DDR4 RAM","DDR SDRAM","DDR2 SDRAM","DDR3 SDRAM","DDR4 SDRAM"]
    intDecision = 0
    while ( (intDecision < 1 ) or (intDecision > len(ramType)) ):
        try:
            print("\nWhat CPU architecture does this unit have?")
            for i in range( len(ramType) ): terminalColor.printBlueString( str(i+1) + ". " + ramType[i])
            intDecision = int(input())
            if ( (intDecision < 1) or (intDecision > len(ramType)) ): terminalColor.printRedString("Invalid Input")
            else: return ramType[intDecision - 1]
        except:
            intDecision = 0
            terminalColor.printRedString("Invalid Input")

def editTextEntry(stuffToUpdate, unitInfo, category):
    originalData = unitInfo[category]
    try: oldData = stuffToUpdate[category]
    except: oldData = unitInfo[category]
    newData = click.edit(oldData)
    newData = newData.replace('\n', '')
    stuffToUpdate[category] = newData
    if originalData == newData: changesMade = False
    elif oldData != newData: changesMade = True
    else: changesMade = False
    return dict(stuffToUpdate=stuffToUpdate, changesMade=changesMade)