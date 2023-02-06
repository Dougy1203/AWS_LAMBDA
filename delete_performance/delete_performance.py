import boto3
from boto3.dynamodb.conditions import Key
dynamo_client = boto3.resource(
    service_name="dynamodb",
    region_name="us-east-1",
    aws_access_key_id="<AWS_ACCESS_KEY_ID>",
    aws_secret_access_key="<AWS_SECRET_ACCESS_KEY>",
)
performance_table = dynamo_client.Table("performances")
print(performance_table.table_status)
director_table = dynamo_client.Table('directors')
print(director_table.table_status)
   
def lambda_handler(event, context):
    request_body = event['body']
    try:
        print('starting your mom')
        res = performance_table.query(
            KeyConditionExpression=Key('uuid').eq(request_body['uuid'])
        )
        response = director_table.query(
            KeyConditionExpression=Key('email').eq(request_body['email'])
        )
        items = response['Items']
        items2 = res['Items']
        director = items[0] if items else None
        validated = True if director['password'] == request_body['password'] else False
        performance = items2[0] if items2 else None
        validated2 = True if performance['uuid'] == request_body['uuid'] else False
        if(validated and validated2):
            response = performance_table.delete_item(Key={
                'uuid': request_body['uuid']
            })
            return {
                'response' : f'Performance Deleted With Name: {performance["name"]}'
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

# lambda_handler({"body" : {
#     'uuid' : '',
#     'email' : '',
#     'password' : '' 
# }}, None)

