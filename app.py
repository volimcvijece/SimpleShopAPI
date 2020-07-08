from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required

from security import authenticate, identity   #funkcije koje smo napisali
from resources.user import UserRegister #UserRegister je nas resource
from resources.item import Item, ItemList
from resources.store import Store, StoreList

"""
request - kad netko napravi req, sacuvaj u var
instalirali smo RESTful, ogranicava kako raditi dobar rest.
Resource je ono sto API nud.
Restful trazi Api(app). Njemu je svaki resource KLASA koja inherita klasu Resource. 
"""

app = Flask(__name__)
#ovo znaci da je baza u root folder naseg projekta
app.config['SQLALCHEMY_DATABASE_URI']=='sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #iskljucujemo sqlacl feature za mod tracker
#za JWT
app.secret_key = 'nekikeykojinesmijebitiukodu'
api = Api(app)

#sa ovim SQL alch radi tablice koje zna, tj vidi u importu. sto nije u importu, nece se napraviti! (uhvati preko resourcea koji linka pak na model)
@app.before_first_request
def create_tables():
    db.create_all()


jwt = JWT(app, authenticate, identity)
#JWT napravi novi endpoint "/auth", kroz to senda usrname i password
#i onda se senda funkciji "AUTHENTICATE" koju smo mi napisali, u njoj
#nademo user object ako je dobro napisano, i tu provjerimo jel pass dobar
#i ako je sve ok, /auth endpoint vraća JTW token
#Taj token bi se trebao slati se requestom i od tad zove drugu funkciju koju smo passali gore, "IDENTITY" funkciju. ako to radi, znaci da je JWT token validan.
#moramo stavljati dekoratore. npr ako poviše geta stavimo @jwt_required(), to znači da se user mora autheticeati PRIJE nego pozove taj get.


api.add_resource(Store, '/store/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(StoreList, '/stores')
#db/orm importamo ispod maina! zbog CIRCULAR IMPORTSA jer gore moduli isto imaju taj import
if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(debug=True)  # important to mention debug=True