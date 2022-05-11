import requests

BASE = "http://127.0.0.1:5000/"

user_wallet = "0x306a430f0e361e96e69d650067eba3f73307b5c4"
rewards = 2

response = requests.get(BASE + "winner")
print(response.json())