from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required

from security import authenticate, identity   
from resources.user import UserRegister 
from resources.item import Item, ItemList
from resources.store import Store, StoreList

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']=='sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 

app.secret_key = 'placeholderkey'
api = Api(app)

@app.before_first_request
def create_tables():
    db.create_all()


jwt = JWT(app, authenticate, identity)
#JWT napravi novi endpoint "/auth", usrnm/psswrd senda prvoj funkciji, token se salje uz request identity funkciji
#potreban dekorator je @jwt_required()


api.add_resource(Store, '/store/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(StoreList, '/stores')

#db import ovdje zbog circular importa
if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(debug=True)  