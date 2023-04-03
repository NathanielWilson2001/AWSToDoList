
import hashlib, boto3, json
from boto3.dynamodb.conditions import Key, Attr

def lambda_handler(event, context):
    accessKey = ""
    secretKey = ""
    sessToken = ""

    
    user = event["Email"]

    dynamodb = boto3.resource('dynamodb', aws_access_key_id = accessKey, aws_secret_access_key = secretKey, aws_session_token = sessToken)

    # Add User Verification: redirect to app 2, check if user exists in
    if(len(user) > 0):
            
        #Verify Account exists, and password matches
        table = dynamodb.Table("tasks")
             
        response = table.query(KeyConditionExpression=Key('email').eq(user))
        try:
            tasks = response['Items']
            return tasks
        except:
            return "FAILURE"