import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel


class UserRegister(Resource):
	#ovo parsa json rikvesta, koristimo ga u def post
	parser = reqparse.RequestParser()
	parser.add_argument('username', type=str, required=True, help="Ovaj field nije blank")
	parser.add_argument('password', type=str, required=True, help="Ovaj field nije blank")

	def post(self):
		data = UserRegister.parser.parse_args()

		if UserModel.find_by_username(data['username']):
			return {'message':'ovaj korisnik vec postoji'}

		user = UserModel(data['username'], data['password'])
		user.save_to_db()

		return {"message": "User created successfully."}, 201
