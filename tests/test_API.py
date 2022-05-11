import requests
from dotenv import load_dotenv
load_dotenv()  # take environment variables from .env.
import os

BASE = "http://127.0.0.1:5000/"
API_PRIVATE_KEY=str(os.environ.get('API_PRIVATE_KEY'))

response = requests.get(BASE + "winner/"+API_PRIVATE_KEY)
print(response.json())