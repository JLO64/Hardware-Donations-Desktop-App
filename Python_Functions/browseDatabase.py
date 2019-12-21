import boto3, json

lambda_client = boto3.client('lambda')

def loginToAWS():
    checkForKey = False
    hasValidCred = False
    if (not checkForKey):
        while(not hasValidCred): hasValidCred = checkCredentials(askForCredentials())

def askForCredentials():
    print("\nPlease type your Hardware Donations Username and Password.\nUsername:", end=" ")
    username = str(input())
    print("Password:", end=" ")
    password = str(input())
    return dict(userToTest=username, passwordToTest=password, type="verify_password")

def checkCredentials(credentials):
    response = lambda_client.invoke(
        FunctionName='arn:aws:lambda:us-west-1:105369739187:function:HDPasswordCheck',
        InvocationType='RequestResponse',
        Payload=json.dumps(credentials),
    )
    passTest=json.loads(response['Payload'].read())
    print(passTest.get('result'))
    return True