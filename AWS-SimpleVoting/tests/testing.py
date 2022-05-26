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
    MNEMONIC_1 = os.environ['MNEMONIC_1']
    testwallet1 = Wallet.fromMnemonic(MNEMONIC_1.split(', '))
    testWallet1_address= testwallet1.getAddress()
    print("Wallet address: " + testWallet1_address)
    print("Wallet VET balance: " + str(connector.get_vet_balance(testWallet1_address)))
    print("Wallet VTHO balance: " + str(connector.get_vtho_balance(testWallet1_address)))
    return testwallet1, testWallet1_address

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

    # First prop will tie with two votes by the same person and another one on "yes" 
    # and two different votes for "no"
    yes_wallet_one= "0xa342a89985b18887f4c6af5b075954c70585ce01"
    no_wallet_one = "0x98521797ccefcd644115bcd53b648aa1da3d18ac"
    #transfer_DHN(connector, DHN_contract_address, testwallet1, receiver_address, amount)

    # Second prop will "win" 3 votes for yes 2 votes for no (one vote extra by one of the same person)
    yes_wallet_two= "0x38a4b0867e7d7d39cfbdbc46e51154033960fa4f"
    no_wallet_two= "0x4193c5a351b9529d5638b2b1e0da37e18dfd3344"

    # Third prop will "lose" 2 votes for yes (two extra votes by the same people) and 3 votes for no
    yes_wallet_three= "0x5f9677093a56b76497d2c77ceff79caa94a66220"
    no_wallet_three= "0xceb037f016a51cdb867421dd810db69492a2a079"