import hashlib, boto3, json

def lambda_handler(event, context):
    accessKey = ""
    secretKey = ""
    sessToken = ""

    email  = event["Email"]
    name = event["Name"]
    description = event["Description"]
    date = event["Date"]

    dynamodb = boto3.resource('dynamodb', aws_access_key_id = accessKey, aws_secret_access_key = secretKey, aws_session_token = sessToken)
    table = dynamodb.Table('tasks')
    
    try:
        response = table.update_item(
        Key={
            'email':email,
            'taskName': name
        },
        UpdateExpression='SET finishDate = :date, description = :description',
        ExpressionAttributeValues={
            ':description': description,
            ':date': date
        },
        ReturnValues='ALL_NEW',
        )

        print(response)
        return response
    except:
         return 'FAILED TO UPDATE'