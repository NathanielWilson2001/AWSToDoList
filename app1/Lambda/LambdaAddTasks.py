import hashlib, boto3, json
from boto3.dynamodb.conditions import Key, Attr

def lambda_handler(event, context):
 
    accessKey = ""
    secretKey = ""
    sessToken = ""
    
    email  = event["Email"]
    name = event["Name"]
    description = event["Description"]
    date = event["Date"]

    # Connections
    dynamodb = boto3.resource('dynamodb', aws_access_key_id = accessKey, aws_secret_access_key = secretKey, aws_session_token = sessToken)
    table = dynamodb.Table('tasks')
    
    response = table.get_item(
             Key={
            'email': email,
            'taskName': name
            }
        ) 
  
    # Check if the response returned with an already existing item under the same name and email
    try:
        if(response["Item"] != None):
            return {"Success" : "ALREADY EXISTS" }

    # If not add, the item and return
    except:
        response = table.put_item(
            Item={
                'email': email,
                'taskName' : name,
                'description': description,
                'finishDate': date,
                'complete': False
                }
            )  
        return {"Success" : "ADDED" }