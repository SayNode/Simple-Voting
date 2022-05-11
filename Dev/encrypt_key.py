#this imports the cryptography package
from base64 import decode
from cryptography.fernet import Fernet

def encryptData(api_key):
    #this just opens your 'key.key' and assings the key stored there as 'key'
    with open('key.key','rb') as file:
        key = file.read()

    #this encrypts the data read from your json and stores it in 'encrypted'
    fernet = Fernet(key)
    encrypted = fernet.encrypt(bytes(api_key, encoding='utf8'))

    #this writes your new, encrypted data into a new JSON file
    return str(encrypted.decode("utf-8"))

def decryptData(api_key):
    #this just opens your 'key.key' and assings the key stored there as 'key'
    with open('key.key','rb') as file:
        key = file.read()

    #this decrypts the data read from your json and stores it in 'encrypted'
    api_key=bytes(api_key, encoding='utf8')
    fernet = Fernet(key)
    decrypted = fernet.decrypt(api_key)

    return decrypted.decode("utf-8")
