import json
import boto3
import uuid
from boto3.dynamodb.conditions import Key


dynamo_client = boto3.resource(
    service_name="dynamodb",
    region_name="us-east-1",
    aws_access_key_id="<AWS_ACCESS_KEY_ID>",
    aws_secret_access_key="<AWS_SECRET_ACCESS_KEY>",
)

director_table = dynamo_client.Table("directors")
print(director_table.table_status)

def lambda_handler(event, context):
    request_body = event['body']
    try:
        print('starting your mom')
        response = director_table.query(
            KeyConditionExpression=Key('email').eq(request_body['email'])
        )
        # print(response)
        items = response['Items']
        email = request_body['email']
        
        if(items):
            return {
                'response' : f'Director Already Exists With Email: "{email}"'
            }
        else:
            director_table.put_item(
                Item={
                    "uuid": str(uuid.uuid4()),
                    "name" : request_body['name'],
                    "email" : request_body['email'],
                    "phoneNumber" : request_body['phoneNumber'],
                    "password" : request_body['password'],
                    "role" : 'director'
                },
            )
            name = request_body['name']
            return{
                'response' : f'Director with name {name} was created successfully'
            }
    except Exception as e:
        print(e)
        return{
            'response' : {
                'status' : 'Internal Server Error---- Try Again',
                'error' : f'{e}'
            }
        }

# lambda_handler({"body" : {
#     "name" : '',
#     "email" : '',
#     "phoneNumber" : '',
#     'password' : ''
# }}, None)