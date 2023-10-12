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