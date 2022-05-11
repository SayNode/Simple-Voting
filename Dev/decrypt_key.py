#this imports the cryptography package
from base64 import decode
from cryptography.fernet import Fernet
from dotenv import load_dotenv
load_dotenv()  # take environment variables from .env.
import os

def decryptData(api_key):
    #this just opens your 'key.key' and assings the key stored there as 'key'
    ENCRYPTION_KEY=str(os.environ.get('ENCRYPTION_KEY'))
    #this decrypts the data read from your json and stores it in 'encrypted'
    api_key=bytes(api_key, encoding='utf8')
    fernet = Fernet(ENCRYPTION_KEY)
    decrypted = fernet.decrypt(api_key)

    return decrypted.decode("utf-8")
