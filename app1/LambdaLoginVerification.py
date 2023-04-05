
import boto3, base64


def lambda_handler(event, context):
    accessKey = ""
    secretKey = ""
    sessToken = ""

  

    user = event["Email"]
    password = event["Password"]
    kmsKey = boto3.client('kms',  region_name= "us-east-1", aws_access_key_id=accessKey,aws_secret_access_key=secretKey, aws_session_token=sessToken)

    dynamodb = boto3.resource('dynamodb', aws_access_key_id = accessKey, aws_secret_access_key = secretKey, aws_session_token = sessToken)
    if(len(user) > 0):
            
        #Verify Account exists, and password matches
        table = dynamodb.Table('users')
             
        response = table.get_item(Key={'email' : user})
        
        #Check if an account with the email address exists, if so, verify the passwords match
        if 'Item' in response:
            plaintext = (kmsKey.decrypt(KeyId="98680603-459b-4a10-83b5-28fe8b8cf205", CiphertextBlob = base64.b64decode(bytes(response['Item']['password']))))
            if plaintext['Plaintext'].decode("utf-8") == password:
                return {"Success" :"true","Name" : response['Item']['name'] }
            else:
                return  {"Success" :"false"}
            
        else:
           return {"Success" :"false"}