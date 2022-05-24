from traceback import print_tb
from thor_requests.connect import Connect
from thor_requests.wallet import Wallet
from thor_requests.contract import Contract
from decouple import config
import requests
import json
import uuid

minAmount = 2
#
#Connect to Veblocks and import the DHN contract
#
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

#
#Get balance
#
def get_balance(connector,_contract, DHN_contract_address, wallet_address):
    balance_one = connector.call(
        caller=wallet_address, # fill in your caller address or all zero address
        contract=_contract,
        func_name="balanceOf",
        func_params=[wallet_address],
        to=DHN_contract_address,
    )
    print("Wallet "+ wallet_address+" DHN balance:" + str(balance_one["decoded"]["0"]))
    return balance_one["decoded"]["0"]

#
# Overwrites the provided JSON file
#
def overwrite_json():

    # Opens the json file
    with open('proposals.json', 'r+') as f:
        data = json.load(f)
        # If the file has already been over writte, it ends the function
        if data['proposals']['1']['yes_wallet'] != "":
            return "Already overwritten"

    # For each proposal inside the json file
    for proposal in data['proposals']:
        with open('proposals.json', 'r+') as f:
            data = json.load(f)
            #Generate yes and no adresses for each proposal
            yes_wallet = Wallet.newWallet().getAddress() # Create a random walle
            no_wallet = Wallet.newWallet().getAddress() # Create a random walle
            data['proposals'][str(proposal)]['yes_wallet'] = yes_wallet 
            data['proposals'][str(proposal)]['no_wallet'] = no_wallet 
            # Generate random ID for each proposal
            data['proposals'][str(proposal)]['id'] = str(uuid.uuid4()) 
            # Just to look good
            f.seek(0)        # <--- should reset file position to the beginning.
            json.dump(data, f, indent=4)
            f.truncate()     # remove remaining part
    
    # Return the overwritten JSON file so it can be used to be called by the front end
    with open('proposals.json', 'r+') as f:
        data = json.load(f)
        return json.dumps(data)

#
# Get the latest block number
#
def latest_block():
    headers = {
    'accept': 'application/json',
    }

    response = requests.get('https://testnet.veblocks.net/blocks/best', headers=headers)
    return response.json()["number"]

#
#Get unique votes of a wallet address
#
def get_unique_votes(connector,_contract, DHN_contract_address, ballot_address, block_init, block_final):
    
    #Removes the "0x" from the address
    ballot_address = ballot_address[2:]

    #Will store the voters addresses
    voters = []

    #Request headers
    headers = {
        'accept': 'application/json'
    }

    json_data = {
        "range": {
            "unit": "block",
            "from": block_init,
            "to": block_final
        },
        "options": {
            "offset": 0,
            "limit": 10000000000
        },
        "criteriaSet": [
            {
                "address": DHN_contract_address,
                "topic2": "0x000000000000000000000000"+ballot_address
            }
        ],
        "order": "asc"
    }

    # Get all txs of money (aka votes) to the specific ballot wallet
    #https://mainnet.veblocks.net/logs/transfer
    response = requests.post('https://testnet.veblocks.net/logs/event', headers=headers, json=json_data)

    # Goes through all the DHN txs the ballot (topic2) received
    for i in range(len(response.json())):
        # Removes the zeros
        voter = "0x"+response.json()[i]["topics"][1][26:]

        #Sees if the voter has already voted (aka if the address is already in the array)
        doesnt_exist = voter not in voters

        #If the voter hasn't voted and has the suffcient balance of DHN
        if doesnt_exist and get_balance(connector,_contract, DHN_contract_address, voter)>minAmount:
            voters.append(voter)

    return len(voters)

#Gets the yes and no ballot wallets for a specific proposal ID
def getWallets(proposal_id):
    # Opens the json file
    with open('proposals.json', 'r+') as f:
        data = json.load(f)
        # If the file has already been over writte, it ends the function
        if data['proposals']['1']['yes_wallet'] == "":
            return "Needs to be overwritten first"

    # For each proposal inside the json file
    for proposal in data['proposals']:
        with open('proposals.json', 'r+') as f:
            data = json.load(f)
            #Get the proposal with the ID we want
            if data['proposals'][str(proposal)]['id'] ==  proposal_id:
                yes_wallet = data['proposals'][str(proposal)]['yes_wallet']
                no_wallet = data['proposals'][str(proposal)]['no_wallet']
                return yes_wallet, no_wallet
    
    return "No proposal found with the id: "+ proposal_id

def winner(proposal_id, block_init, block_final):
    #Connect
    (connector, _contract, DHN_contract_address) = init()

    #If there is no specified last block, than the last block processed is considered the last one
    if block_final=="None":
        block_final = latest_block()

    #Get yes and no ballot wallets corresponding to the requested proposal id
    (yes_ballot_address, no_ballot_address) = getWallets(proposal_id)
    
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
    overwrite_json()
    
#main()
(connector,_contract, DHN_contract_address)=init()
#print(get_unique_votes(connector,_contract, DHN_contract_address, '0x306A430F0E361e96E69D650067Eba3F73307b5C4', 0, latest_block()))
print(getWallets("4be2a58f-931d-49aa-af14-cd2047bba153"))