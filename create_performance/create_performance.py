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
director_table = dynamo_client.Table("directors")
    
def lambda_handler(event, context):
    request_body = event['body']
    try:
        print("starting your mom")
        response = director_table.query(
            KeyConditionExpression=Key('email').eq(request_body['d_email'])
        )
        cdResponse = director_table.query(
            KeyConditionExpression=Key('email').eq(request_body['cd_email'])
        )
        d_items = response['Items']
        cd_items = cdResponse['Items']
        director = None
        cDirector = None
        if(d_items and cd_items):
            print("directors exist")
            director = d_items[0]
            cDirector = cd_items[0]
            if(director['password'] == request_body['password']):
                print('validated')
                performance_table.put_item(
                Item={
                    "uuid": str(uuid.uuid4()),
                    "title": request_body['title'],
                    "director": director,
                    "castingDirector": cDirector,
                    "dates": json.dumps(request_body['dates']),
                    "characters": json.dumps(request_body['characters']),
                    "venue": request_body['venue'],
                    "auditions" : json.dumps(request_body['auditions']),
                    "cast" : json.dumps(request_body['cast'])
                    },
                )
                return {
                    'response' : f'Performance Successfully Created: {request_body["title"]}'
                }
            else:
                print('not validated')
                return {
                    'response' : 'Validation Information Incorrect---- Try Again'
                }
    except Exception as e:
        return{
            'response' : {
                'status' : 'Internal Server Error---- Try Again',
                'error' : f'{e}'
            }
        }

# lambda_handler({"body" : {
#     "d_email" : "",
#     "cd_email" : "",
#     "password" : "",
#     "title": "",
#     "dates": [],
#     "characters": [],
#     "venue": "",
#     "auditions" : [],
#     "cast" : {}
# }}, None)