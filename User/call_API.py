import requests
from dotenv import load_dotenv
load_dotenv()  # take environment variables from .env.
import os

from encrypt_key import *

BASE = "http://127.0.0.1:5000/"
API_PRIVATE_KEY=str(os.environ.get('API_PRIVATE_KEY'))

block_init = input("Input the beggining block:")

response = requests.get(BASE + "winner/"+str(block_init)+'/'+ encryptData(API_PRIVATE_KEY))
print(response.json())
