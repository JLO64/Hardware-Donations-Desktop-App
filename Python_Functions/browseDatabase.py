import boto3, json, getpass
import terminalColor, settingsJson

lambda_client = boto3.client('lambda')

def loginToAWS():
    if not hasValidCredStored():
        askForCredentials()
    else:
        hasValidCred = checkCredentials(dict(userToTest=settingsJson.username, passwordToTest=settingsJson.password, type="verify_password"))
        if hasValidCred: selectCategory()
        while not hasValidCred: askForCredentials()

def askForCredentials(): #Ask user for login info
    hasValidCred = False
    while(not hasValidCred):
        try:
            print("\nPlease type your Hardware Donations Username and Password.(Type \"Cancel\" to exit)\nUsername:", end=" ")
            username = str(input())
            if username.lower()=="cancel": break
            password = getpass.getpass(prompt="Password(Input Hidden): ")
            if password.lower()=="cancel": break
            hasValidCred = checkCredentials(dict(userToTest=username, passwordToTest=password, type="verify_password"))
            if hasValidCred:
                settingsJson.username = username
                settingsJson.password = password
                selectCategory()
        except:
            terminalColor.printRedString("Invalid Input")


def checkCredentials(credentials): #Connect to AWS Lambda to check login
    response = lambda_client.invoke(
        FunctionName='arn:aws:lambda:us-west-1:105369739187:function:HDPasswordCheck',
        InvocationType='RequestResponse',
        Payload=json.dumps(credentials),
    )
    passTest=json.loads(response['Payload'].read())
    if (passTest.get('result')): terminalColor.printGreenString("Login Successful")
    else: terminalColor.printRedString("Login Failed")
    return passTest.get('result')

def selectCategory():
    intDecision = 0
    listOfOptions =[". Search Units", ". Search Users", ". Exit"]
    while ( (intDecision < 1 ) or (intDecision > len(listOfOptions)) ):
        try:
            print("\nWhat do you want to do?")
            for i in range( len(listOfOptions) ): terminalColor.printBlueString( str(i+1) + listOfOptions[i] )
            intDecision = int(input())
            if ( (intDecision < 1) or (intDecision > len(listOfOptions)) ): terminalColor.printRedString("Invalid Input")
            elif ( listOfOptions[intDecision-1] == ". Exit"): break
        except:
            intDecision = 0
            terminalColor.printRedString("Invalid Input")

def hasValidCredStored():
    if( settingsJson.username == "na" and settingsJson.password == "na" ):
        return False
    else:
        return True