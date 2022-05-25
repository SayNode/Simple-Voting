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

	def get(self, api_key):
		PRIVATE_KEY = str(os.environ['API_PRIVATE_KEY'])
		if PRIVATE_KEY != api_key:
			abort(401, message="Wrong API key")	
		return vechain_txs.winner()

class CurrentVotes(Resource):
		
	def get(self, proposal_id, api_key):
		PRIVATE_KEY = str(os.environ['API_PRIVATE_KEY'])
		if PRIVATE_KEY != api_key:
			abort(401, message="Wrong API key")	
		(yes_wallet, no_wallet)=vechain_txs.getWallets(proposal_id)
		yes = vechain_txs.get_unique_votes(yes_wallet)
		no = vechain_txs.get_unique_votes(no_wallet)
		return yes, no		

class UploadProposals(Resource):
		
	def post(self, api_key):
		PRIVATE_KEY = str(os.environ['API_PRIVATE_KEY'])
		if PRIVATE_KEY != api_key:
			abort(401, message="Wrong API key")	
		return 200	


api.add_resource(Winner, "/winner/<string:api_key>")
api.add_resource(CurrentVotes, "/CurrentVotes/<string:proposal_id>/<string:api_key>")
api.add_resource(UploadProposals, "/UploadProposals/<string:fileName>/<string:api_key>")

if __name__ == "__main__":
	application.run()