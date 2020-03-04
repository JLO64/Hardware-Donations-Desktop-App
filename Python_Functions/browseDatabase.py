import boto3, json, getpass, os, click
import terminalColor, settingsJson, fileFunctions, unitEdit

lambda_client = boto3.client('lambda')

def loginToAWS():
    if not hasValidCredStored():
        if askForCredentials(True): selectCategory()
    else:
        hasValidCred = checkCredentials(dict(key1=settingsJson.key1, key2=settingsJson.key2, key3=settingsJson.key3, type="verify_key"))
        if hasValidCred: selectCategory()
        else:
            hasValidCred = askForCredentials(True)

def askForCredentials(storeCredentials): #Ask user for login info
    hasValidCred = False
    wantsToCancel = False
    while(not hasValidCred and not wantsToCancel):
        try:
            print("\nPlease enter your Email and Password.(Type \"Cancel\" to exit)\nEmail:", end=" ")
            username = str(input())
            if username.lower()=="cancel":
                wantsToCancel = True
                break
            password = getpass.getpass(prompt="Password(Input Hidden): ")
            if password.lower()=="cancel":
                wantsToCancel = True
                break
            hasValidCred = checkCredentials(dict(username=username, password=password, type="verify_password"))
            if hasValidCred:
                if storeCredentials: askToSaveLoginInfo()
                return True
            else:
                terminalColor.printRedString("Login Failed")
                return False
        except:
            terminalColor.printRedString("Invalid Input")
    return False


def checkCredentials(credentials): #Connect to AWS Lambda to check login
    response = lambda_client.invoke(
        FunctionName='arn:aws:lambda:us-west-1:105369739187:function:HDPasswordCheck',
        InvocationType='RequestResponse',
        Payload=json.dumps(credentials),
    )
    passTest=json.loads(response['Payload'].read())
    if (passTest.get('result')):
        terminalColor.printGreenString("Login Successful")
        settingsJson.key1 = passTest.get('key1')
        settingsJson.key2 = passTest.get('key2')
        settingsJson.key3 = passTest.get('key3')
        return True
    else: return False

def selectCategory():
    intDecision = 0
    listOfOptions =[". Search Units", ". Search Users", ". Create Unit", ". Exit"]
    while ( (intDecision < 1 ) or (intDecision > len(listOfOptions)) ):
        try:
            print("\nWhat do you want to do?")
            for i in range( len(listOfOptions) ): terminalColor.printBlueString( str(i+1) + listOfOptions[i] )
            intDecision = int(input())
            if ( (intDecision < 1) or (intDecision > len(listOfOptions)) ): terminalColor.printRedString("Invalid Input")
            elif ( listOfOptions[intDecision-1] == ". Exit"): break
            elif ( listOfOptions[intDecision-1] == ". Search Units"):
                intDecision = 0
                searchResults = searchUnits()
                if searchResults["unitExists"]: unitEdit.unitEditOptions(searchResults["rJSON"], searchResults["unitID"])
                else: terminalColor.printRedString("unable to find unit")
            elif ( listOfOptions[intDecision-1] == ". Create Unit"):
                intDecision = 0
                createUnit()
        except:
            intDecision = 0
            terminalColor.printRedString("Invalid Input")

def hasValidCredStored():
    if readSavedCredentials() or ( not settingsJson.key1 == "na" ):
        return True
    else:
        return False

def searchUnits():
    unitTypeInt = 0
    unitNumInt = 0
    unitType = ""
    unitID = ""
    listOfUnitTypes =[". HDD", ". HDL", ". NX", ". Exit"]
    while ( (unitTypeInt < 1 ) or (unitTypeInt > len(listOfUnitTypes)) ):
        try:
            print("\nWhat unit type do you want to search for?")
            for i in range( len(listOfUnitTypes) ): terminalColor.printBlueString( str(i+1) + listOfUnitTypes[i] )
            unitTypeInt = int(input())
            if ( (unitTypeInt < 1) or (unitTypeInt > len(listOfUnitTypes)) ): terminalColor.printRedString("Invalid Input")
            elif ( listOfUnitTypes[unitTypeInt-1] == ". Exit"): break
            elif ( listOfUnitTypes[unitTypeInt-1] == ". HDD"): unitType = "HDD"
            elif ( listOfUnitTypes[unitTypeInt-1] == ". HDL"): unitType = "HDL"
            elif ( listOfUnitTypes[unitTypeInt-1] == ". NX"): unitType = "NX"
            print("\nWhat unit number do you want to search for?")
            print(unitType + "-", end="")
            unitNumInt = int(input())
            unitID = unitType + "-" + str(unitNumInt)
            responseJson = getUnitInfo(unitID)
            if (responseJson["result"] == True ): return dict(unitExists=True, rJSON=responseJson, unitID=unitID)
            else: return dict(unitExists=False, unitID=unitID)
        except:
            unitTypeInt = 0
            terminalColor.printRedString("Invalid Input")

def getUnitInfo(unitID):
    payload = dict(key1=settingsJson.key1, key2=settingsJson.key2, key3=settingsJson.key3, type="unit_info", unitID=unitID)
    response = lambda_client.invoke(
        FunctionName='arn:aws:lambda:us-west-1:105369739187:function:HDPasswordCheck',
        InvocationType='RequestResponse',
        Payload=json.dumps(payload),
    )
    responseJson = json.loads(response['Payload'].read())
    return responseJson

def askToSaveLoginInfo():
    saveChoice = 0
    listOfChoices =[". Yes", ". No"]
    while ( (saveChoice < 1 ) or (saveChoice > len(listOfChoices)) ):
        try:
            print("Do want to save your login credentials?")
            for i in range( len(listOfChoices) ): terminalColor.printBlueString( str(i+1) + listOfChoices[i] )
            saveChoice = int(input())
            if ( (saveChoice < 1) or (saveChoice > len(listOfChoices)) ): terminalColor.printRedString("Invalid Input")
            elif ( listOfChoices[saveChoice-1] == ". No"): break
            elif ( listOfChoices[saveChoice-1] == ". Yes"):
                fileFunctions.checkForDirectory( os.path.expanduser('~') + "/HardwareDonations/Settings" )
                jsonToSave = dict(key1=settingsJson.key1, key2=settingsJson.key2, key3=settingsJson.key3)
                with open( os.path.expanduser('~') + "/HardwareDonations/Settings/LoginInfo", 'w') as outfile:
                    json.dump(jsonToSave, outfile)
                terminalColor.printGreenString("Login credentials saved")
        except:
            saveChoice = 0
            terminalColor.printRedString("Invalid Input")

def readSavedCredentials():
    if fileFunctions.checkForFile(os.path.expanduser('~') + "/HardwareDonations/Settings/LoginInfo"):
        with open(os.path.expanduser('~') + "/HardwareDonations/Settings/LoginInfo") as json_file:
            data = json.load(json_file)
            settingsJson.key1 = data.get('key1')
            settingsJson.key2 = data.get('key2')
            settingsJson.key3 = data.get('key3')
            return True
    else: return False

def createUnit():
    print("\nPlease enter the following information")
    searchResults = searchUnits()
    if searchResults["unitExists"]: 
        terminalColor.printRedString("This unit already exists")
        return
    unitID = searchResults["unitID"]
    terminalColor.printGreenString("No unit located with this id")
    jsonTemplate = {}
    listOfCategories = ["Location", "Status", "UserID", "Manufacturer", "Model", "ARK-OS_Version", "Operating System", "CPU Type", "CPU GHz", "CPU Threads","CPU Architecture","RAM","RAM Slots","RAM Type", "HDD", "HDD Port","HDD Speed","USB Ports","Audio Ports","Display Ports","Disk Drive","Networking","Ports", "Comments"]
    for i in listOfCategories: jsonTemplate[i] = "NO DATA"
    newUnitJSON =  unitEdit.unitEditEntry( dict(unitInfo=jsonTemplate), "Creating New Unit")
    if newUnitJSON["Unit_ID"] == "OkToUpload":
        newUnitJSON["Unit_ID"] = unitID
        unitType = unitID.split("-",1)[0]
        if unitType == "HDD": newUnitJSON["Category"] = "HDD(Hardware Donations Desktop)"
        elif unitType == "HDL": newUnitJSON["Category"] = "HDL(Hardware Donations Laptop)"
        elif unitType == "NX": newUnitJSON["Category"] = "NX(Experimental)"
        payload = dict(key1=settingsJson.key1, key2=settingsJson.key2, key3=settingsJson.key3, type="unit_create", unitID=unitID, unitInfo=newUnitJSON)
        response = lambda_client.invoke(
            FunctionName='arn:aws:lambda:us-west-1:105369739187:function:HDPasswordCheck',
            InvocationType='RequestResponse',
            Payload=json.dumps(payload),
        )
        passTest=json.loads(response['Payload'].read())
        if passTest["result"]: terminalColor.printGreenString("Unit Successfully created")
        else: terminalColor.printRedString("Unit creation failed")
    else:
        terminalColor.printRedString("Unit creation canceled")