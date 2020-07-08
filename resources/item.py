from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

#ovdje smo prije imali classmethode, ali ovo je resurs, konzumira se
#a metode ne konzumira api direktno nego mi to radimo unutar koda, logicnije je to preseliti
#Zato ima vise smisla staviti u models
class Item(Resource):
    TABLE_NAME = 'items'

    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help="This field cannot be left blank!"
    )

     parser.add_argument('store_id',
        type=int,
        required=True,
        help="Every item needs a store id!"
    )


    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json() 
        return {'message': 'Item not found'}, 404

   

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': "An item with name '{}' already exists.".format(name)}

        data = Item.parser.parse_args()

        #item = {'name': name, 'price': data['price']}
        item = ItemModel(name, data['price'])
        try:
            item.save_to_db()
        except:
            return {"message": "An error occurred inserting the item."}

        return item

    

    @jwt_required()
    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
        return{'message': 'item deleted'}

    @jwt_required()
    def put(self, name):
        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)
        
        #ako je none, saveaj u db
        if item is None:
            item = ItemModel(name, data['price'], data['store_id'])
        else:
            item.price = data['price']
            #item.store_id = data['store_id']
        item.save_to_db()
        return item.json()




class ItemList(Resource):
    TABLE_NAME = 'items'

    def get(self):
                #list(map(lambda x:x.json(), ItemModel.query.all())) - umjesto pythonic nacina list comprehensiona, mocan nacin
        return {'items': [item.json() for item in ItemModel.query.all()]}
