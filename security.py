from models.user import UserModel

#importali smo klasu User iz user.py
#prije smo imali rjecnik, sad imamo db pa imamo custom funkcije u user.py
def authenticate(username, password):
	user = UserModel.find_by_username(username)
	if user and user.password == password:
		return user

#ovo je jedinstveno instaliranoj JTW ekstenziji
#ova funkc uzima PAYLOAD a to je content JTW tokena, 
#i mi ekstrahiramo user id iz tog payloada
def identity(payload):
	user_id=payload['identity']
	return UserModel.find_by_id(user_id)

	
