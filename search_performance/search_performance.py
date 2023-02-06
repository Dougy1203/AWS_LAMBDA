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

performance_table = dynamo_client.Table("performances")
performer_table = dynamo_client.Table("performers")
print(performance_table.table_status)
print(performer_table.table_status)

def lambda_handler(event, context):
    request_body = event['body']
    try:
        print("starting your mom")
        response = performance_table.query(
            KeyConditionExpression=Key('uuid').eq(request_body['uuid'])
        )
        res = performer_table.query(
            KeyConditionExpression=Key('email').eq(request_body['email'])
        )
        items = response['Items']
        items2 = res['Items']
        performance = items[0] if items else None
        performer = items2[0] if items2 else None
        validated = True if (performer['password'] == request_body['password']) and performance else False
        if(validated):
            title = performance['title']
            characters = json.loads(performance['characters'])
            print(title)
            print(characters)
            return {
                "title" : title,
                "characters" : json.dumps(characters)
            }
        else:
            return {
                'response' : 'Validation Error---- Try Again'
            }
    except Exception as e:
        return{
            'response' : {
                'status' : 'Internal Server Error---- Try Again',
                'error' : f'{e}'
            }
        }

# lambda_handler({'body' : {
#     'email' : '',
#     'password' : '',
#     'uuid' : ''
# }}, None)