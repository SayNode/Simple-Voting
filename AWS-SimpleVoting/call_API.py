import requests
from dotenv import load_dotenv
load_dotenv()  # take environment variables from .env.
import os

BASE = "https://simplevoteapi-env.eba-qmpvtfpj.eu-central-1.elasticbeanstalk.com/"
API_PRIVATE_KEY=str(os.environ.get('API_PRIVATE_KEY'))

""" block_init = input("Input the beggining block:")
block_end=input("Input the final block (if you wish to use the last processed block write 'None'):") """

response = requests.get(BASE + "winner/"+str(0)+'/'+ "None"+'/'+ API_PRIVATE_KEY)

print(response.json())
