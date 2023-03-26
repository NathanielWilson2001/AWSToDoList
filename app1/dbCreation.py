import boto3

accessKey = ""
secretKey = ""
sessToken = ""

# Get the service resource.
dynamodb = boto3.resource('dynamodb', aws_access_key_id= accessKey, aws_secret_access_key= secretKey, aws_session_token=sessToken)

# Create the DynamoDB table.
userTable = dynamodb.create_table(
    TableName='users',
    KeySchema=[
        {
            'AttributeName': 'email',
            'KeyType': 'HASH'
        }
    ],
    AttributeDefinitions=[
        {
            'AttributeName': 'email',
            'AttributeType': 'S'
        }
    ],
    ProvisionedThroughput={
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    }
)

toDoListtable = dynamodb.create_table(
    TableName='tasks',
    KeySchema=[
        {
            'AttributeName': 'email',
            'KeyType': 'HASH'
        },
        {
            'AttributeName': 'taskName',
            'KeyType': 'RANGE'
        }
    ],
    AttributeDefinitions=[
        {
            'AttributeName': 'email',
            'AttributeType': 'S'
        },
       {
            'AttributeName': 'taskName',
             'AttributeType': 'S'
        }
    ],
    ProvisionedThroughput={
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    }
)
