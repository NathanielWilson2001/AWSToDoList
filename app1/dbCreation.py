import boto3

accessKey = "ASIA6AONFUCHEHVYHA25"
secretKey = "m5H/cS1unHOl+Vz1MNwPwzVFwmN1PP7IRul9MZD9"
sessToken = "FwoGZXIvYXdzEOb//////////wEaDKfqP+xEf21MXtpZ/iLAAZC9+o1gFH5+7pHB+zII2Uyp06xwVnA5/hZZl5AH/8Opr04Ye0sT4QZRaVdmaWC5PbksLe+fYYrHB8AKVzN87Q4aATRq2bn+okZ5SWD722hkgymUAvfVIkbDuLqb2/0cjG/OZbXipGEonTyw544Cabb8e1BJ/PCx6UBb4+/U6KTIijFucUdPuvpqapXSeueHuJBBk6IoPC9QTNBSpHwqbr5TWGRDQKyDFLRoCkhiHvntemtvT0uvhekSiJsLBk2RFSi4x9qhBjItJlfx62VLQ69KQD3vYUOfteYOwXs6CkCi8HUOgbFHhq34HvRzvrnNihDX3o13"

# Get the service resource.
dynamodb = boto3.resource('dynamodb', aws_access_key_id= accessKey, aws_secret_access_key= secretKey, aws_session_token=sessToken)

# Create the DynamoDB table.
userTable = dynamodb.create_table(
    TableName='user',
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
    TableName='task',
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
