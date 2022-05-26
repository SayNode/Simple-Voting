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
    print("------------------Connect to Veblocks------------------\n")
    #https://mainnet.veblocks.net
    #SayNode testnet node : http://3.71.71.72:8669/doc/swagger-ui/
    #SayNode mainnet node : http://3.124.193.149:8669/doc/swagger-ui/
    connector = Connect("http://3.71.71.72:8669")
    print("------------------IMPORT DHN CONTRACT------------------\n")
    _contract = Contract.fromFile("./build/contracts/DHN.json")
    DHN_contract_address = '0x0867dd816763BB18e3B1838D8a69e366736e87a1'
    return connector, _contract, DHN_contract_address

#Import wallets from mnemonic (this should be only one, but for know we need 2 for testing)
def wallet_import_1(connector):
    #MNEMONIC_1 = config('MNEMONIC_1')
    MNEMONIC_1 = config('MNEMONIC_1')
    testwallet1 = Wallet.fromMnemonic(MNEMONIC_1.split(', '))
    testWallet1_address= testwallet1.getAddress()
    print("Wallet address: " + testWallet1_address)
    print("Wallet VET balance: " + str(connector.get_vet_balance(testWallet1_address)))
    print("Wallet VTHO balance: " + str(connector.get_vtho_balance(testWallet1_address)))
    return testwallet1, testWallet1_address

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

def transfer_DHN(connector, DHN_contract_address, testwallet1, receiver_address, amount):
    connector.transfer_token(
        testwallet1, 
        to=receiver_address,
        token_contract_addr= DHN_contract_address, 
        amount_in_wei=amount
    )

def main():
    (connector, _contract, DHN_contract_address)=init()
    (testwallet1, testWallet1_address)=wallet_import_1(connector)
    wallet_two='0x306A430F0E361e96E69D650067Eba3F73307b5C4'
    wallet_three='0x5007d0568127Bd998010Aa5a094361cE75B68B5f'
    wallet_four='0x00712682a3aF33187570b41937A384A390DE7799'
    wallet_five='0x72a3e156EB026b6e21327A22C8E4BB239464Eb6D'
    wallet_six='0x9150BBa5E4875076cE98fa35EcEdD6A87f8598C6'

    transfer_DHN(connector, DHN_contract_address, testwallet1, wallet_two, 2)
    transfer_DHN(connector, DHN_contract_address, testwallet1, wallet_three, 2)
    transfer_DHN(connector, DHN_contract_address, testwallet1, wallet_four, 2)
    transfer_DHN(connector, DHN_contract_address, testwallet1, wallet_five, 2)
    transfer_DHN(connector, DHN_contract_address, testwallet1, wallet_six, 2)

    time.sleep(15)
    get_balance(connector,_contract, DHN_contract_address, testWallet1_address,1)
    get_balance(connector,_contract, DHN_contract_address, wallet_two, 2)
    get_balance(connector,_contract, DHN_contract_address, wallet_three, 3)
    get_balance(connector,_contract, DHN_contract_address, wallet_four, 4)
    get_balance(connector,_contract, DHN_contract_address, wallet_five, 5)
    get_balance(connector,_contract, DHN_contract_address, wallet_six, 6)

main()
