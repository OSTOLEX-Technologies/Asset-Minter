# import boto3
import os
import json
from web3 import Web3


private_key = os.environ.get("PRIVATE_KEY")
if private_key is None:
    raise Exception("PRIVATE_KEY environment variable is not set")
# sqs = boto3.client('sqs')

# queue_url = 'SQS_QUEUE_URL'

web3 = Web3(Web3.HTTPProvider('https://testnet.aurora.dev'))

while not web3.is_connected():  
    print(web3.is_connected())

with open("abi.json", 'r') as abi_file:
    contract_abi = json.load(abi_file)

contract_address = '0x483809d2Af8f3Aa5794b19547dcc2e76dD8B2075'
account_address = '0xE225445094069a2A358aeE252E91603CfAD9DBdc'

contract = web3.eth.contract(address=contract_address, abi=contract_abi)

def mint(address, token_type_id):
    function_name = "safeMint"
    function_args = [address, token_type_id]
    transaction_params = {
        "from": account_address,
        "nonce" : web3.eth.get_transaction_count(account_address),
        "gasPrice": web3.eth.gas_price,
        "gas": 200000
    }

    nonce = web3.eth.get_transaction_count(account_address)

    transaction = contract.functions.safeMint(address, 1).build_transaction(transaction_params)
    signed_txn = web3.eth.account.sign_transaction(transaction, private_key)
    
    tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    
    web3.eth.wait_for_transaction_receipt(tx_hash)
    
    tx_receipt = web3.eth.get_transaction_receipt(tx_hash)
    
    print(tx_receipt)
    # print(transaction)



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

mint("0xE225445094069a2A358aeE252E91603CfAD9DBdc", 1)
