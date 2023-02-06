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
director_table = dynamo_client.Table('directors')
performer_table = dynamo_client.Table('performers')

def lambda_handler(event, context):
    request_body = event['body']
    try:
        print("starting your mom")
        performance = performance_table.query(
            KeyConditionExpression = Key('uuid').eq(request_body['uuid'])
        )['Items'][0]
        director = director_table.query(
            KeyConditionExpression = Key('email').eq(request_body['director_email'])
        )['Items'][0]
        performer = performer_table.query(
            KeyConditionExpression = Key('email').eq(request_body['performer_email'])
        )['Items'][0]
        validation = True if director['password'] == request_body['password'] else False
        characters = json.loads(performance['characters'])
        if(validation and (request_body['character_name'] in characters)):
            cast = json.loads(performance['cast'])
            cast[request_body['character_name']] = performer['name']
            characters.remove(request_body['character_name'])
            auditions = json.loads(performance['auditions'])
            auditions.remove(performer['name'])
            print(cast)
            print(characters)
            performance_table.update_item(
                Key={
                    'uuid': request_body['uuid'],
                },
                UpdateExpression='SET #ts = :val1, #ts2 = :val2, #ts3 = :val3',
                ExpressionAttributeValues={
                  ":val1": json.dumps(cast),
                  ":val2": json.dumps(characters),
                  ":val3": json.dumps(auditions)
                },
                ExpressionAttributeNames={
                  "#ts": "cast",
                  "#ts2": "characters",
                  "#ts3": "auditions"
                }
            )
            performer_table.update_item(
                Key={
                    'email': request_body['performer_email'],
                },
                UpdateExpression='SET #ts = :val1',
                ExpressionAttributeValues={
                  ":val1": performance['title']
                },
                ExpressionAttributeNames={
                  "#ts": "cp"
                }
            )
            performerName = performer['name']
            characterName = request_body['character_name']
            return {
              'response' : f'{performerName} has been cast for {characterName}'
            }

    except Exception as e:
        return{
            'response' : {
                'status' : 'Internal Server Error---- Try Again',
                'error' : f'{e}'
            }
        }

# lambda_handler({'body' : {
#     'director_email' : '',
#     'password' : '',
#     'character_name' : '',
#     'performer_email' : '',
#     'uuid' : ''
# }}, None)