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

def lambda_handler(event, context):
    request_body = event['body']
    try:
        print("starting your mom")
        response = performer_table.query(
            KeyConditionExpression=Key('email').eq(request_body['email'])
        )
        items = response['Items']
        performer = items[0] if items else None
        validated = True if performer['password'] == request_body['password'] else False
        if(validated):
            pp = json.loads(performer['pp'])
            pp.append(request_body['pp'])
            performer_table.update_item(
                Key={
                    'email': request_body['email'],
                },
                UpdateExpression='SET pp = :val1',
                ExpressionAttributeValues={
                    ':val1': json.dumps(pp)
                }
            )
            return{
                'response' : f"{performer['name']} Added Performance: {request_body['pp']}"
            }
        else:
            return{
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
#     'pp' : ''
# }}, None)