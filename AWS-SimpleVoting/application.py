from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
import vechain_txs 
import os

application = Flask(__name__)
api = Api(application)

@application.route('/')
def index():
    return 'Unidentified API'

class Winner(Resource):

	def get(self, block_ini, block_end, api_key):
		PRIVATE_KEY = str(os.environ['API_PRIVATE_KEY'])
		if PRIVATE_KEY != api_key:
			abort(401, message="Wrong API key")	
		return vechain_txs.main(block_ini, block_end)

class CurrentVotes(Resource):
		
	def get(self, block_ini, block_end, api_key):
		PRIVATE_KEY = str(os.environ['API_PRIVATE_KEY'])
		if PRIVATE_KEY != api_key:
			abort(401, message="Wrong API key")	
		return vechain_txs.main(block_ini, block_end)		

class UploadProposals(Resource):
		
	def post(self, block_ini, block_end, api_key):
		PRIVATE_KEY = str(os.environ['API_PRIVATE_KEY'])
		if PRIVATE_KEY != api_key:
			abort(401, message="Wrong API key")	
		return vechain_txs.main(block_ini, block_end)	


api.add_resource(Winner, "/winner/<string:block_ini>/<string:block_end>/<string:api_key>")

if __name__ == "__main__":
	application.run()