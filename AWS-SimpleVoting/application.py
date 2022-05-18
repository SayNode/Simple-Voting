from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
import vechain_txs 
from dotenv import load_dotenv
load_dotenv()  # take environment variables from .env.
import os

application = Flask(__name__)
api = Api(application)
API_PRIVATE_KEY=str(os.environ.get('API_PRIVATE_KEY'))

class Form(Resource):
	
	def get(self, block_ini, API_KEY):
			
		return vechain_txs.main(block_ini)
		


api.add_resource(Form, "/winner/<int:block_ini>/<string:API_KEY>")

if __name__ == "__main__":
	application.run()