import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

class Item(Resource):
	#ovo je REQPARSE, request parsing. stavili smo ga u klasu a ne unutar metode, PRIMIJETITI kako nismo dodali self., jer bez tog sad ovo pripada cijeloj klasi a ne nekoj class resource, tako da možemo unutar metoda zvati sa Item.parser.parse_args()
	parser = reqparse.RequestParser()
	parser.add_argument('price', type=float, required=True, help="Ovaj field ne moze biti blank")


	@jwt_required()
	def get(self, name):
		#filter vrati filter object, trebamo ga konvertirati
		#next daje prvi item kojeg nade filter function
		#ovo je kao for item, if item[name]==name
		#ali next moze baciti error ako nema rezultata, pa moramo dodati onaj , None (ako ne findaj, vrati None
		item = next(filter(lambda x: x['name'] == name, item), None)
		#return {'student':name}, 200 if item  else 404

	def post(self, name):

		#data = request.get_json()
		#kod bez ovog next ce raditi ali ce dati error ako req nema content type header ili ako nije json, radi toga trebamo napisati bolji kod radi ERROR CONTROL (odmah ispod)
		if next(filter(lambda x: x['name']==name, items), None):
			return{'message':"Item '{}' vec postoji".format(name)}, 400
		#ovdje je data jer nema smisla uzimati na početku ako ovaj 			if poviše daje error!
		data = Item.parser.parse_args()
		#data = request.get_json()
		item = {'name': name, 'price': data['price']}
		#items.append(item) 
		#return item, 201

	def delete(self, name):
		global items #ovako dohvatimo items izvan funkcije/klase!!!
		#inace bi bio error, ovaj items ne bi nista povukao!
		items = list(filter(lambda x: x['name'] !=name, items))
		return {'message': 'item se izbrisao'}

	def put(self, name):
		data = Item.parser.parse_args()
		item = next(filter(lambda x: x['name'] == name, items), None)
		if item is None:
			item = {'name': name, 'price': data['price']}
			items.append(item)
		else:
			item.update(data)
		return item

class ItemList(Resource):
	def get(self):
		return{'items':items}