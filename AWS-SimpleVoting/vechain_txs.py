from thor_requests.connect import Connect
from thor_requests.wallet import Wallet
from thor_requests.contract import Contract
from decouple import config
import requests
import json
import time

#Get the latest block number
def latest_block():
    headers = {
    'accept': 'application/json',
    }

    response = requests.get('https://testnet.veblocks.net/blocks/best', headers=headers)
    return response.json()["number"]

#Get votes
def get_unique_votes(ballot_address, block_init, block_final):
    
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

        if exists:
            voters.append(i['sender'])

    return len(voters)

def winner(yes_ballot_address, no_ballot_address, block_init, block_final):
    #If there is no specified last block, than the last block processed is considered the last one
    if block_final=="None":
        block_final = latest_block()

    #Get unique votes for each of the ballot wallets
    yes = get_unique_votes(yes_ballot_address, int(block_init), int(block_final))
    no = get_unique_votes(no_ballot_address, int(block_init), int(block_final))

    # Announce who won
    if yes>no:
        return "The proposal was approved"
    elif no>yes:
        return "The proposal was rejected"

    return "The voting ended in a tie"


def main(block_ini, block_end):

    yes_ballot_address = '0x2652000025cDb4bc1A9296117F0EEF8cf14b5f3b'
    no_ballot_address = '0x54E09Bf67B215f2Bbe8c33310148d2f070a66218'

    return winner(yes_ballot_address, no_ballot_address, block_ini, block_end)
""" block_init = input("Input the beggining block:")
block_end=input("Input the final block (if you wish to use the last processed block write 'None'):")
print(main(block_init,block_end)) """