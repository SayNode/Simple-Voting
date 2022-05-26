from traceback import print_tb
from thor_requests.connect import Connect
from thor_requests.wallet import Wallet
from thor_requests.contract import Contract
from decouple import config
import requests
import json
import os
import time
from decouple import config

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

def get_balance(connector,_contract, DHN_contract_address, wallet_address, num):

    #Call balance function
    balance_one = connector.call(
        caller=wallet_address, # fill in your caller address or all zero address
        contract=_contract,
        func_name="balanceOf",
        func_params=[wallet_address],
        to=DHN_contract_address,
    )
    print("Wallet"+str(num)+" "+ wallet_address+" DHN balance:" + str(balance_one["decoded"]["0"]))
    return balance_one["decoded"]["0"]

def get_ballot_balance(connector,_contract, DHN_contract_address, wallet_address):

    #Call balance function
    balance_one = connector.call(
        caller=wallet_address, # fill in your caller address or all zero address
        contract=_contract,
        func_name="balanceOf",
        func_params=[wallet_address],
        to=DHN_contract_address,
    )
    print("Wallet "+ wallet_address+" DHN balance:" + str(balance_one["decoded"]["0"]))
    return balance_one["decoded"]["0"]

def transfer_DHN(connector, DHN_contract_address, testwallet1, receiver_address, amount):
    connector.transfer_token(
        testwallet1, 
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

    print("Vote balances")
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
    
    get_ballot_balance(connector,_contract, DHN_contract_address, yes_wallet_one)
    get_ballot_balance(connector,_contract, DHN_contract_address, no_wallet_one)
    get_ballot_balance(connector,_contract, DHN_contract_address, yes_wallet_two)
    get_ballot_balance(connector,_contract, DHN_contract_address, no_wallet_two)
    get_ballot_balance(connector,_contract, DHN_contract_address, yes_wallet_three)
    get_ballot_balance(connector,_contract, DHN_contract_address, no_wallet_three)
    
    """ print("4) TRANSFERS")
    transfer_DHN(connector, DHN_contract_address, testwallet1, testWallet2_address, 2)
    transfer_DHN(connector, DHN_contract_address, testwallet1, testWallet3_address, 2)
    transfer_DHN(connector, DHN_contract_address, testwallet1, testWallet4_address, 2)
    transfer_DHN(connector, DHN_contract_address, testwallet1, testWallet5_address, 2)
    transfer_DHN(connector, DHN_contract_address, testwallet1, testWallet6_address, 200)

    time.sleep(10)
    print("5) BALANCES")
    get_balance(connector,_contract, DHN_contract_address, testWallet1_address,1)
    get_balance(connector,_contract, DHN_contract_address, testWallet2_address, 2)
    get_balance(connector,_contract, DHN_contract_address, testWallet3_address, 3)
    get_balance(connector,_contract, DHN_contract_address, testWallet4_address, 4)
    get_balance(connector,_contract, DHN_contract_address, testWallet5_address, 5)
    get_balance(connector,_contract, DHN_contract_address, testWallet6_address, 6)  """

main()
