import json
import boto3
import uuid
from boto3.dynamodb.conditions import Key, Attr


dynamo_client = boto3.resource(
    service_name="dynamodb",
    region_name="us-east-1",
    aws_access_key_id="<AWS_ACCESS_KEY_ID>",
    aws_secret_access_key="<AWS_SECRET_ACCESS_KEY>",
)

performer_table = dynamo_client.Table("performers")
print(performer_table.table_status)

def lambda_handler(event, context):
    request_body = event['body']
    try:
        print('starting your mom')
        response = performer_table.query(
            KeyConditionExpression=Key('email').eq(request_body['email'])
        )
        items = response['Items']
        email = request_body['email']
        
        if(items):
            return {
                'response' : f'Performer Already Exists With Email: "{email}"'
            }
        else:
            performer_table.put_item(
                Item={
                    "uuid": str(uuid.uuid4()),
                    "name" : request_body['name'],
                    "email" : request_body['email'],
                    "phoneNumber" : request_body['phoneNumber'],
                    "pp" : json.dumps(request_body['pp']),
                    "cp" : request_body['cp'],
                    'password' : request_body['password'],
                    "role" : 'performer'
                },
            )
            return{
                'response' : f'Performer Successfully Created With Name: {request_body["name"]}'
            }
    except Exception as e:
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
#     'password' : '',
#     "pp" : [],
#     "cp" : ''
# }}, None)