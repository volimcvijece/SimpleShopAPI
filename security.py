from models.user import UserModel


def authenticate(username, password):
	user = UserModel.find_by_username(username)
	if user and user.password == password:
		return user

#JWT ekstenzija - payload je content JTW tokena, treba vratiti user id iz payloada
def identity(payload):
	user_id=payload['identity']
	return UserModel.find_by_id(user_id)

	
