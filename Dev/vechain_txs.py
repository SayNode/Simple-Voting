from thor_requests.connect import Connect
from thor_requests.wallet import Wallet
from thor_requests.contract import Contract
from decouple import config
import requests
import json
import time

#Connect to Veblocks and import the DHN contract
def init():

    connector = Connect("https://testnet.veblocks.net")

    return connector

#Import wallets from mnemonic (this should be only one, but for know we need 2 for testing)
def wallet_import_1(connector):
    MNEMONIC_1 = config('MNEMONIC_1')
    testwallet1 = Wallet.fromMnemonic(MNEMONIC_1.split(', '))
    testWallet1_address= testwallet1.getAddress()
    print("Wallet address: " + testWallet1_address)
    print("Wallet VET balance: " + str(connector.get_vet_balance(testWallet1_address)))
    print("Wallet VTHO balance: " + str(connector.get_vtho_balance(testWallet1_address)))
    return testwallet1, testWallet1_address

def wallet_import_2(connector):
    MNEMONIC_2 = config('MNEMONIC_2')
    testwallet2 = Wallet.fromMnemonic(MNEMONIC_2.split(', '))
    testWallet2_address= testwallet2.getAddress()
    print("Wallet address: " + testWallet2_address)
    print("Wallet VET balance: " + str(connector.get_vet_balance(testWallet2_address)))
    print("Wallet VTHO balance: " + str(connector.get_vtho_balance(testWallet2_address)))
    return testwallet2, testWallet2_address

def wallet_import_3(connector):
    MNEMONIC_3 = config('MNEMONIC_3')
    testwallet3 = Wallet.fromMnemonic(MNEMONIC_3.split(', '))
    testWallet3_address= testwallet3.getAddress()
    print("Wallet address: " + testWallet3_address)
    print("Wallet VET balance: " + str(connector.get_vet_balance(testWallet3_address)))
    print("Wallet VTHO balance: " + str(connector.get_vtho_balance(testWallet3_address)))
    return testwallet3, testWallet3_address

def ballot_wallet_balance(connector,_contract, DHN_contract_address, ballot_addr):
    print("Ballot:")
    balance_one = connector.call(
        caller=ballot_addr, # fill in your caller address or all zero address
        contract=_contract,
        func_name="balanceOf",
        func_params=[ballot_addr],
        to=DHN_contract_address,
    )
    print(balance_one["decoded"]["0"])
#Get wallet balances, we use "call" in order to not waste any gas (once again this should be separated, but it will be done when ready 
# to deploy)
def wallet_balance(connector,_contract, DHN_contract_address, testWallet1_address, testWallet2_address, testWallet3_address):
    print("Wallet1:")
    balance_one = connector.call(
        caller=testWallet1_address, # fill in your caller address or all zero address
        contract=_contract,
        func_name="balanceOf",
        func_params=[testWallet1_address],
        to=DHN_contract_address,
    )
    print(balance_one["decoded"]["0"])

    print("Wallet2:")
    balance_two = connector.call(
        caller=testWallet2_address, # fill in your caller address or all zero address
        contract=_contract,
        func_name="balanceOf",
        func_params=[testWallet2_address],
        to=DHN_contract_address,
    )
    print(balance_two["decoded"]["0"]) 

    print("Wallet3:")
    balance_three = connector.call(
        caller=testWallet3_address, # fill in your caller address or all zero address
        contract=_contract,
        func_name="balanceOf",
        func_params=[testWallet3_address],
        to=DHN_contract_address,
    )
    print(balance_three["decoded"]["0"]) 
def latest_block():
    headers = {
    'accept': 'application/json',
    }

    response = requests.get('https://testnet.veblocks.net/blocks/best', headers=headers)
    return response.json()["number"]

#Get votes
def get_unique_votes(ballot_address, block_init, block_final):
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

    response = requests.post('https://testnet.veblocks.net/logs/transfer', headers=headers, json=json_data)
    for i in response.json():
        print(i['sender'])
    return 0

def winner( yes_ballot_address, no_ballot_address, block_init, block_final ):
    get_unique_votes(yes_ballot_address, block_init, block_final)
    get_unique_votes(no_ballot_address, block_init, block_final)



def main():
    print("------------------Connect to Veblocks------------------")
    connector=init()

    yes_ballot_address = '0x2652000025cDb4bc1A9296117F0EEF8cf14b5f3b'
    no_ballot_address = '0x54E09Bf67B215f2Bbe8c33310148d2f070a66218'

    print(get_unique_votes<('0x306A430F0E361e96E69D650067Eba3F73307b5C4', 0, latest_block()))
    #print(winner(yes_ballot_address,  no_ballot_address,0, 12216178))


"""     print("------------------WALLET 1------------------\n")
    (testwallet1, testWallet1_address)=wallet_import_1(connector)
    print("------------------WALLET 2------------------\n")
    (testwallet2, testWallet2_address)=wallet_import_2(connector)
    print("------------------WALLET 3------------------\n")
    (testwallet3, testWallet3_address)=wallet_import_3(connector)

    print("------------------CREATE BALLOT WALLETS------------------\n")
    (yes_wallet, no_wallet) = create_Ballot_Wallets()
    print(yes_wallet.getAddress())

    print("------------------DHN Balances Before Transfer------------------\n")
    wallet_balance(connector,_contract, DHN_contract_address, testWallet1_address, testWallet2_address, testWallet3_address)

    print("------------------Votes------------------\n")
    vote(connector, DHN_contract_address, testWallet1_address,yes_wallet, no_wallet, 2)
    vote(connector, DHN_contract_address, testWallet2_address,yes_wallet, no_wallet, 1)
    vote(connector, DHN_contract_address, testWallet3_address,yes_wallet, no_wallet, 2)

    #Sleep for 10 seconds to allow for the tx to be processed
    time.sleep(10)

    print("------------------DHN Balances After Transfer------------------\n")
    wallet_balance(connector,_contract, DHN_contract_address, testWallet1_address, wallet_id) """
main()