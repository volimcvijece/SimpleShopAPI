import sqlite3
from db import db

#model je INTERNA reprezentacija, tako da mora imati
#propertije tog itema kao object propertije
class ItemModel(db.Model):
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(80))
	price = db.Column(db.Float(precision=2))
    store_id=db.Column(db.Integer, db.ForeignKey('stores.id')) #stores je table name, id je column
    store = db.relationship('StoreModel')

    def __init__(self, name, price, store_id):
        self.name = name
        self.price = price
        self.store_id = store_id

    def json(self):
        return {'name':self.name, 'price':self.price}

    #cls je referenca klase
    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first() #sqlalch carolija, SELECT * FROM items WHERE name=name LIMIT 1
        #ovaj cls je u biti ova klasa, ItemModel, jer ovo je classmethod
    #prije smo imali za ovo class metod i cls, ali ima VISE SMISLA da je self jer inserta sam u sebe!!!!
    
    #ovo je "upserting", radi kao update i kao insert
    def save_to_db(self):
        db.session.add(self) #session je kolekcija objekta koji writeamo u bazu
        db.session.commit()

    #prije smo imali za ovo class metod i cls, ali ima VISE SMISLA da je self jer apdejta sam u sebe!!!!
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()