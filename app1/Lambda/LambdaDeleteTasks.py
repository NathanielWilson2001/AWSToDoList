import  boto3

def lambda_handler(event, context):
    
    accessKey = ""
    secretKey = ""
    sessToken = ""
    
    email  = event["Email"]
    name = event["Name"]
   
   # Attempt to delete an item from the tasks table, return finish if it finishes, failure if it does not
    try:
        dynamodb = boto3.resource('dynamodb', aws_access_key_id = accessKey, aws_secret_access_key = secretKey, aws_session_token = sessToken)
        table = dynamodb.Table('tasks')
        response = table.delete_item(
            Key={
                 'email':email,
                 'taskName': name
                },
            )
        return "FINISH"
    except:
        return "FAILURE"