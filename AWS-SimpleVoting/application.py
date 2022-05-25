from flask import Flask, request, jsonify
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
import vechain_txs 
import os
import json

application = Flask(__name__)
api = Api(application)

@application.route('/')
def index():
    return 'Unidentified API'

# Post the new proposals
class UploadProposals(Resource):
		
	def post(self, api_key):
		PRIVATE_KEY = str(os.environ['API_PRIVATE_KEY'])
		if PRIVATE_KEY != api_key:
			abort(401, message="Wrong API key")	

		#Get the JSON info sent with the POST request
		proposals_JSON = request.get_json()

		#Open the file in the API server and writting in it what was sent in the POST req
		with open('proposals.json', 'r+') as f:
			data = proposals_JSON
			f.seek(0)        # <--- should reset file position to the beginning.
			json.dump(data, f, indent=4)
			f.truncate()     # remove remaining part
			#Creates ballot wallets and proposals IDs
			return vechain_txs.overwrite_json()

# Request current votes
class CurrentVotes(Resource):
		
	def get(self, proposal_id, api_key):
		PRIVATE_KEY = str(os.environ['API_PRIVATE_KEY'])
		if PRIVATE_KEY != api_key:
			abort(401, message="Wrong API key")	

		#See if the proposal voting has already been closed. In that case, it skips calculating
		#the votes and just provides the final ones
		with open('proposals.json', 'r+') as f:
			data = json.load(f)
			# For each proposal inside the json file
			for proposal in data['proposals']:
				#Get the proposal with the ID we want
				if data['proposals'][str(proposal)]['id'] ==  proposal_id and data['proposals'][str(proposal)]['status'] ==  "finished":
					return {"id" : proposal_id,
							"yes_votes": data['proposals'][str(proposal)]['final_yes_votes'],
				 			"no_votes": data['proposals'][str(proposal)]['final_no_votes']}	

		#If the proposal voting is still on-going
		#get the ballot wallets
		(yes_wallet, no_wallet)=vechain_txs.getWallets(proposal_id)
		#calculate their votes
		yes = vechain_txs.get_unique_votes(yes_wallet)
		no = vechain_txs.get_unique_votes(no_wallet)
		return {"id" : proposal_id,
				"yes_votes": str(yes),
				 "no_votes": str(no)}	

#Gets the current JSON info
class JSONInfo(Resource):

	def get(self, api_key):
		PRIVATE_KEY = str(os.environ['API_PRIVATE_KEY'])
		if PRIVATE_KEY != api_key:
			abort(401, message="Wrong API key")
		with open('proposals.json', 'r+') as f:
			data = json.load(f)
			return data	

# Request Winner
class Winner(Resource):

	def get(self, api_key):
		PRIVATE_KEY = str(os.environ['API_PRIVATE_KEY'])
		if PRIVATE_KEY != api_key:
			abort(401, message="Wrong API key")	
		# Calculates the winners and updates the JSON file in the API server
		return vechain_txs.winner()

api.add_resource(UploadProposals, "/UploadProposals/<string:api_key>")
api.add_resource(CurrentVotes, "/CurrentVotes/<string:proposal_id>/<string:api_key>")
api.add_resource(JSONInfo, "/JSONInfo/<string:api_key>")
api.add_resource(Winner, "/Winner/<string:api_key>")

if __name__ == "__main__":
	application.run()