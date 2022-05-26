from traceback import print_tb
from thor_requests.connect import Connect
from thor_requests.wallet import Wallet
from thor_requests.contract import Contract
from decouple import config
import requests
import json
import os

minAmount = 2
#
#Connect to Veblocks and import the DHN contract
#
def init():
    print("1) Connect to Veblocks")
    #https://mainnet.veblocks.net
    #SayNode testnet node : http://3.71.71.72:8669/doc/swagger-ui/
    #SayNode mainnet node : http://3.124.193.149:8669/doc/swagger-ui/
    connector = Connect("http://3.71.71.72:8669")
    print("2) IMPORT DHN CONTRACT")
    _contract = Contract.fromFile("./build/contracts/DHN.json")
    DHN_contract_address = '0x0867dd816763BB18e3B1838D8a69e366736e87a1'
    return connector, _contract, DHN_contract_address

#Import wallets from mnemonic (this should be only one, but for know we need 2 for testing)
def wallet_import(num):
    mne = 'MNEMONIC_'+str(num)
    MNEMONIC = config(mne)
    testwallet = Wallet.fromMnemonic(MNEMONIC.split(', '))
    testWallet_address= testwallet.getAddress()
    return testwallet, testWallet_address

def transfer_DHN(connector, DHN_contract_address, testwallet, receiver_address, amount):
    connector.transfer_token(
        testwallet, 
        to=receiver_address,
        token_contract_addr= DHN_contract_address, 
        amount_in_wei=amount
    )

def main():
    (connector, _contract, DHN_contract_address)=init()
    
    print("3) WALLETs CONNECTION")
    (testwallet1, testWallet1_address)=wallet_import(1)
    (testwallet2, testWallet2_address)=wallet_import(2)
    (testwallet3, testWallet3_address)=wallet_import(3)
    (testwallet4, testWallet4_address)=wallet_import(4)
    (testwallet5, testWallet5_address)=wallet_import(5)
    (testwallet6, testWallet6_address)=wallet_import(6)

    with open('proposals.json', 'r+') as f:
        data = json.load(f)
        # For each proposal inside the json file
        for proposal in data['proposals']:
            if int(proposal) == 1:
                yes_wallet_one= data['proposals'][str(proposal)]["yes_wallet"]
                no_wallet_one = data['proposals'][str(proposal)]["no_wallet"]
            if int(proposal) == 2:
                yes_wallet_two= data['proposals'][str(proposal)]["yes_wallet"]
                no_wallet_two= data['proposals'][str(proposal)]["no_wallet"]
            if int(proposal) == 3:
                yes_wallet_three= data['proposals'][str(proposal)]["yes_wallet"]
                no_wallet_three= data['proposals'][str(proposal)]["no_wallet"]

    # First prop will tie with two votes by the same person and another one on "yes" 
    # and two different votes for "no"
    transfer_DHN(connector, DHN_contract_address, testwallet1, yes_wallet_one, 1)#1-0
    transfer_DHN(connector, DHN_contract_address, testwallet1, yes_wallet_one, 1)#1-0
    transfer_DHN(connector, DHN_contract_address, testwallet2, yes_wallet_one, 1)#2-0
    transfer_DHN(connector, DHN_contract_address, testwallet3, no_wallet_one, 1)#2-1
    transfer_DHN(connector, DHN_contract_address, testwallet4, no_wallet_one, 1)#2-2
    

    # Second prop will "win" 3 votes for yes 2 votes for no (one vote extra by one of the same person)
    transfer_DHN(connector, DHN_contract_address, testwallet1, yes_wallet_two, 1)#1-0
    transfer_DHN(connector, DHN_contract_address, testwallet2, yes_wallet_two, 1)#2-0
    transfer_DHN(connector, DHN_contract_address, testwallet3, yes_wallet_two, 1)#3-0
    transfer_DHN(connector, DHN_contract_address, testwallet4, no_wallet_two, 1)#3-1
    transfer_DHN(connector, DHN_contract_address, testwallet4, no_wallet_two, 1)#3-1
    transfer_DHN(connector, DHN_contract_address, testwallet5, no_wallet_two, 1)#3-2

    # Third prop will "lose" 2 votes for yes (two extra votes by the same people) and 3 votes for no
    transfer_DHN(connector, DHN_contract_address, testwallet1, yes_wallet_three, 1)#1-0
    transfer_DHN(connector, DHN_contract_address, testwallet2, yes_wallet_three, 1)#2-0
    transfer_DHN(connector, DHN_contract_address, testwallet1, yes_wallet_three, 1)#2-0
    transfer_DHN(connector, DHN_contract_address, testwallet2, yes_wallet_three, 1)#2-0
    transfer_DHN(connector, DHN_contract_address, testwallet4, no_wallet_three, 1)#2-1
    transfer_DHN(connector, DHN_contract_address, testwallet5, no_wallet_three, 1)#2-2
    transfer_DHN(connector, DHN_contract_address, testwallet6, no_wallet_three, 1)#2-3

main()