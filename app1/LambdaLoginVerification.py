
import hashlib, boto3, json

def lambda_handler(event, context):
    accessKey = ""
    secretKey = ""
    sessToken = ""
    
    user = event["Email"]
    password = event["Password"]
    
    dynamodb = boto3.resource('dynamodb', aws_access_key_id = accessKey, aws_secret_access_key = secretKey, aws_session_token = sessToken)
    if(len(user) > 0):
            
        #Verify Account exists, and password matches
        table = dynamodb.Table('users')
             
        response = table.get_item(
            Key={
                'email': user
                }
            )
        try:
            account = response['Item']
            if(account['email'] == user and account['password'] == password):
                return "SUCCESS"
            else:
                return "Invalid Email or Password"
        except:
            return user, password, response, "FAILURE"