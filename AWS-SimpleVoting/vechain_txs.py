from traceback import print_tb
from thor_requests.connect import Connect
from thor_requests.wallet import Wallet
from thor_requests.contract import Contract
from decouple import config
import requests
import json
import uuid

minAmount = 2
#Connect to Veblocks and import the DHN contract
def init():
    print("------------------Connect to Veblocks------------------\n")
    #https://mainnet.veblocks.net
    #SayNode testnet node : http://3.71.71.72:8669/doc/swagger-ui/
    #SayNode mainnet node : http://3.124.193.149:8669/doc/swagger-ui/
    connector = Connect("http://3.71.71.72:8669")
    print("------------------IMPORT DHN CONTRACT------------------\n")
    _contract = Contract.fromFile("./build/contracts/DHN.json")
    DHN_contract_address = '0x0867dd816763BB18e3B1838D8a69e366736e87a1'
    return connector, _contract, DHN_contract_address

#Get balance
def get_balance(connector,_contract, DHN_contract_address, wallet_address):
    print("Wallet "+ wallet_address+" DHN balance:")
    balance_one = connector.call(
        caller=wallet_address, # fill in your caller address or all zero address
        contract=_contract,
        func_name="balanceOf",
        func_params=[wallet_address],
        to=DHN_contract_address,
    )
    return balance_one["decoded"]["0"]

#Create Wallets
def overwrite_json():

    # Writing to sample.json
    with open('proposals.json', 'r+') as f:
        data = json.load(f)
    for proposal in data['proposals']:
        with open('proposals.json', 'r+') as f:
            data = json.load(f)
            yes_wallet = Wallet.newWallet().getAddress() # Create a random walle
            no_wallet = Wallet.newWallet().getAddress() # Create a random walle
            data['proposals'][str(proposal)]['yes_wallet'] = yes_wallet # <--- add `id` value.
            data['proposals'][str(proposal)]['no_wallet'] = no_wallet # <--- add `id` value.
            data['proposals'][str(proposal)]['id'] = str(uuid.uuid4()) # <--- add `id` value.
            f.seek(0)        # <--- should reset file position to the beginning.
            json.dump(data, f, indent=4)
            f.truncate()     # remove remaining part

#Get the latest block number
def latest_block():
    headers = {
    'accept': 'application/json',
    }

    response = requests.get('https://testnet.veblocks.net/blocks/best', headers=headers)
    return response.json()["number"]

#Get votes
def get_unique_votes(connector,_contract, DHN_contract_address, ballot_address, block_init, block_final):
    
    voters = []

    headers = {
        'accept': 'application/json'
    }

    json_data = {
        'range': {
            'unit': 'block',
            'from': block_init,
            'to': block_final,
        },
        'options': {
            'offset': 0,
            'limit': 10,
        },
        'criteriaSet': [
            {
                'recipient': ballot_address,
            },
        ],
        'order': 'asc'
    }

    # Get all txs of money (aka votes) to the specific ballot wallet
    #https://mainnet.veblocks.net/logs/transfer
    response = requests.post('https://testnet.veblocks.net/logs/transfer', headers=headers, json=json_data)

    # Gets the unique voter from the collected data
    for i in response.json():
        exists = i['sender'] not in voters

        #If this wallet address hasn't been registered and the wallet balance of DHN is greater then the minimum amount
        if exists and get_balance(connector,_contract, DHN_contract_address, i['sender'])>minAmount:
            voters.append(i['sender'])

    return len(voters)

def winner(yes_ballot_address, no_ballot_address, block_init, block_final):
    #Connect
    (connector, _contract, DHN_contract_address) = init()

    #If there is no specified last block, than the last block processed is considered the last one
    if block_final=="None":
        block_final = latest_block()

    #Get unique votes for each of the ballot wallets
    yes = get_unique_votes(connector,_contract, DHN_contract_address,yes_ballot_address, int(block_init), int(block_final))
    no = get_unique_votes(connector,_contract, DHN_contract_address,no_ballot_address, int(block_init), int(block_final))

    # Announce who won
    if yes>no:
        return "The proposal was approved"
    elif no>yes:
        return "The proposal was rejected"

    return "The voting ended in a tie"


def main():

    yes_ballot_address = '0x2652000025cDb4bc1A9296117F0EEF8cf14b5f3b'
    no_ballot_address = '0x54E09Bf67B215f2Bbe8c33310148d2f070a66218'
    overwrite_json()
    
main()