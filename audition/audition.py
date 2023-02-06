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

def lambda_handler(event, context):
    request_body = event['body']
    try:
        print("starting your mom")
        response = performer_table.query(
            KeyConditionExpression=Key('email').eq(request_body['email'])
        )
        items = response["Items"]
        p_response = performance_table.query(
            KeyConditionExpression=Key('uuid').eq(request_body['uuid'])
        )
        p_items = p_response["Items"]
        performance = p_items[0] if p_items else None
        performer = items[0] if items else None
        p_validation = True if performance else False
        print(p_validation)
        isAuditioned = True if performer['name'] in json.loads(performance['auditions']) else False
        print(isAuditioned)
        validation = True if performer['password'] == request_body['password'] else False
        print(validation)
        if((validation and p_validation) and not isAuditioned):
            auditions = json.loads(performance['auditions'])
            auditions.append(performer['name'])
            performance_table.update_item(
                Key={
                    'uuid': request_body['uuid'],
                },
                UpdateExpression='SET auditions = :val1',
                ExpressionAttributeValues={
                    ':val1': json.dumps(auditions)
                }
            )
            name = performer['name']
            perfName = performance['name']
            return {
                "response" : f'{name} has Auditioned for {perfName}'
            }
        else:
            return {
                "response" : "Error in Validation Information: Try Again"
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