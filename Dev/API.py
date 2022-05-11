from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
import vechain_txs 
import encrypt_key
from dotenv import load_dotenv
load_dotenv()  # take environment variables from .env.
import os

app = Flask(__name__)
api = Api(app)
API_PRIVATE_KEY=str(os.environ.get('API_PRIVATE_KEY'))

class Form(Resource):
	
	def get(self, API_KEY):
		
		if encrypt_key.decryptData(API_KEY) == API_PRIVATE_KEY:
			vechain_txs.main()
			return "Done"
		return "Incorrect API Key"


api.add_resource(Form, "/winner/<string:API_KEY>")

if __name__ == "__main__":
	app.run()