import boto3
import json

sqs = boto3.client('sqs')

queue_url = 'SQS_QUEUE_URL'


response = sqs.receive_message(
    QueueUrl=queue_url,
    AttributeNames=[
        'SentTimestamp'
    ],
    MaxNumberOfMessages=1,
    MessageAttributeNames=[
        'All'
    ],
    VisibilityTimeout=0,
    WaitTimeSeconds=0
)

def mint(address, token_type_id):
    #TODO: Add logic
    print(f"Minting {token_type_id} tokens to {address}")

def process_message(message):
    body = json.loads(message['Body'])
    address = body.get('address')
    token_type_id = body.get('token_type_id')

    mint(address, token_type_id)