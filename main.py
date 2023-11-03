# import boto3
import os
import json
from web3 import Web3
from web3.auto import w3
from typing import Union

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}



def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

private_key = os.environ.get("PRIVATE_KEY")
if private_key is None:
    raise Exception("PRIVATE_KEY environment variable is not set")

# sqs = boto3.client('sqs')

# queue_url = 'SQS_QUEUE_URL'
rpc_url = os.environ.get("RPC_URL")
web3 = Web3(Web3.HTTPProvider(rpc_url))

while not web3.is_connected():  
    print(web3.is_connected())

with open("abi.json", 'r') as abi_file:
    contract_abi = json.load(abi_file)

contract_address = os.environ.get("CONTRACT_ADDRESS")
account_address = w3.eth.account.from_key(private_key).address # os.environ.get("ACCOUNT_ADDRESS")

if contract_address is None:
    raise Exception("CONTRACT_ADDRESS environment variable is not set")

if account_address is None:
    raise Exception("ACCOUNT_ADDRESS environment variable is not set")

contract = web3.eth.contract(address=contract_address, abi=contract_abi)

@app.get("/mint")
def mint(address_to: str, token_uri: str):
    print(address_to, token_uri)
    function_name = "safeMint"
    function_args = [address_to, token_uri]
    transaction_params = {
        "from": account_address,
        "nonce" : web3.eth.get_transaction_count(account_address),
        "gasPrice": web3.eth.gas_price,
        "gas": 250000
    }

    nonce = web3.eth.get_transaction_count(account_address)

    transaction = contract.functions.safeMint(address_to, token_uri).build_transaction(transaction_params)
    signed_txn = web3.eth.account.sign_transaction(transaction, private_key)
    
    tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    
    web3.eth.wait_for_transaction_receipt(tx_hash)
    
    tx_receipt = web3.eth.get_transaction_receipt(tx_hash)
    
    print(tx_receipt)
    # print(transaction)



def lambda_function(event, context):
    for record in event['Records']:
        attributes = record['messageAttributes']
        address_to = attributes['address_to']['stringValue']
        token_uri = attributes['token_uri']['stringValue']
        mint(address=address_to, token_uri=token_uri)


# mint("0xE225445094069a2A358aeE252E91603CfAD9DBdc", 1)
