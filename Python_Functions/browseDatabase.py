import boto3

def loginToAWS():
    print("\nPlease type your Hardware Donations Username and Password.\nUsername:", end=" ")
    username = str(input())
    print("Password:", end=" ")
    password = str(input())
