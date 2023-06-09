import json, boto3, hashlib, base64
from boto3.dynamodb.conditions import Key, Attr

def lambda_handler(event, context):
    
    accessKey = ""
    secretKey = ""
    sessToken = ""
    
    kmsKey =  boto3.client('kms',  region_name= "us-east-1", aws_access_key_id=accessKey,aws_secret_access_key=secretKey, aws_session_token=sessToken)
    
    email = event["Email"]
    password = event["Password"]
    name = event["Name"]
    
    # Encrypt with KMS
    password = (kmsKey.encrypt(KeyId="98680603-459b-4a10-83b5-28fe8b8cf205", Plaintext = password))
    password = password['CiphertextBlob']
    
    dynamodb = boto3.resource('dynamodb', aws_access_key_id= accessKey, aws_secret_access_key= secretKey, aws_session_token = sessToken)
    
    # If the password or email are not long enough, return
    if len(name) == 0 or len(password) == 0:
        return {"Success" :"false"} 
    else:  
            
        # Add Verify if an account with a similar username already exists, if not create account, redirect to login   
        table = dynamodb.Table('users')
        response = table.query(KeyConditionExpression=Key('email').eq(str(email)))
        try:
            if(response['Count'] > 0):
               return {"Success" :"false"}
            else:   
                table.put_item(
                    Item={
                        'email': email,
                        'name' : name,
                        'password': base64.b64encode(password)
                        },
                )  
                return {"Success" :"true"}
            
        except:
            return {"Success" :"false"}
            
            