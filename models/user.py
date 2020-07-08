import sqlite3 

#ovo nije resurs vec MODEL - to je interna reprezentacija entiteta. realno helper za fleksibilnost da ne trpamo sve u resource.
#RESURS je EKSTERNA reprezentacija entiteta sa kojima klijent komunicira
#ubacili smo ORM pa ekstenda db.Model, ali prije smo radili bez toga
#(btw, ovo je isto api, nije rest ali je api i exposea dvije metode, findbyusername i findbyid)
class UserModel(db.Model):
	__tablename__ = 'users'
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(80))
	password = db.Column(db.String(80))

	#gore su ORM polja, dolje su ona od klase koja ce se sacuvati u db
	#ovdje nema id-a jer je gore autoincrementan
	def __init__(self, username, password):
		self.username = username
		self.password = password
		#_id jer je id py keyword pa samo da zaobidemo

	def save_to_db(self):
		db.session.add(self)
		db.session.commit()

	#classmethod nije potreban ali je bolji, u def pozivamo User objekt
	#pa je logicnije ga pozvati kao cls(row[0])... nego unutar klase pozvati istu
	@classmethod
	def find_by_username(cls, username):
		return cls.query.filter_by(username=username).first() #SELECT * FROM users WHERE username=username LIMIT 1

	@classmethod
	def find_by_id(cls, _id):
		return cls.query.filter_by(id=_id).first() 


#ova gornja User klasa NE SMIJE biti ista kao User RESOURCE, zato imamo ispod ovo
#kojeg dodajemo u api, tj kao api.add_resource(UserRegister, '/register')
