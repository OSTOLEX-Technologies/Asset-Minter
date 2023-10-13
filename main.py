import boto3
import json
from privatekey import private_key
from web3 import Web3

sqs = boto3.client('sqs')

queue_url = 'SQS_QUEUE_URL'

web3 = Web3(Web3.HTTPProvider('https://testnet.aurora.dev'))

with open("abi.json", 'r') as abi_file:
    contract_abi = json.load(abi_file)

contract_address = '0x483809d2Af8f3Aa5794b19547dcc2e76dD8B2075'
account_address = '0xE225445094069a2A358aeE252E91603CfAD9DBdc'

contract = web3.eth.contract(address=contract_address, abi=contract_abi)

def mint(address, token_type_id):
    function_name = "safe_mint"
    function_args = []
    transaction = {
        "from": account_address,
        "to": contract_address,
        "gasPrice": web3.eth.gas_price
    }
    


def process_message(message):
    body = json.loads(message['Body'])
    address = body.get('address')
    token_type_id = body.get('token_type_id')

    mint(address, token_type_id)

def handler(event, context):
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

    if 'Messages' in response:
        for message in response['Messages']:
            process_message(message)

            receipt_handle = message['ReceiptHandle']
            sqs.delete_message(
                QueueUrl=queue_url,
                ReceiptHandle=receipt_handle
            )

    return {
        'statusCode': 200,
        'body': json.dumps('Messages processed')
    }
