#this imports the cryptography package
from base64 import decode
from cryptography.fernet import Fernet
from dotenv import load_dotenv
load_dotenv()  # take environment variables from .env.
import os

def encryptData(api_key):
    #this just opens your 'key.key' and assings the key stored there as 'key'
    ENCRYPTION_KEY=str(os.environ.get('ENCRYPTION_KEY'))
    #this encrypts the data read from your json and stores it in 'encrypted'
    fernet = Fernet(ENCRYPTION_KEY)
    encrypted = fernet.encrypt(bytes(api_key, encoding='utf8'))

    #this writes your new, encrypted data into a new JSON file
    return str(encrypted.decode("utf-8"))
