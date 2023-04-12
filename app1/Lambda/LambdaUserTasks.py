
import hashlib, boto3, json
from boto3.dynamodb.conditions import Key, Attr

def lambda_handler(event, context):
    
    accessKey = ""
    secretKey = ""
    sessToken = ""
    
    user = event["Email"]
    dynamodb = boto3.resource('dynamodb', aws_access_key_id = accessKey, aws_secret_access_key = secretKey, aws_session_token = sessToken)

    # Checks if email is long enough
    if(len(user) > 0):
        
        # Grab all tasks from response table that match the email    
        table = dynamodb.Table("tasks")
        response = table.query(KeyConditionExpression=Key('email').eq(user))
        try:
            tasks = response['Items']
            return tasks
        except:
            return "FAILURE"