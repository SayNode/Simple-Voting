from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
import vechain_txs 
from dotenv import load_dotenv
load_dotenv()  # take environment variables from .env.
import os

application = Flask(__name__)
api = Api(application)

@application.route('/')
def index():
    return 'Unidentified API'

class Form(Resource):
	
	def get(self, block_ini, block_end, api_key):
		PRIVATE_KEY = str(os.environ.get('PRIVATE_KEY'))
		if PRIVATE_KEY != api_key:
			abort(401, message="Wrong API key")	
		return vechain_txs.main(block_ini, block_end)
		


api.add_resource(Form, "/winner/<int:block_ini>/<int:block_end>/<string:API_KEY>")

if __name__ == "__main__":
	application.run()