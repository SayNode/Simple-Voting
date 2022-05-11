from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
import vechain_txs 

app = Flask(__name__)
api = Api(app)

class Form(Resource):
	
	def get(self):
		vechain_txs.main()
		return "Done"


api.add_resource(Form, "/winner")

if __name__ == "__main__":
	app.run(debug=True)