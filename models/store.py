from db import db

#model je INTERNA reprezentacija, tako da mora imati
#propertije tog itema kao object propertije
class StoreModel(db.Model):
    __tablename__ = 'stores'
    id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(80))

    #back reference prema keyu, nakon ovog pogleda u ItemModel koji je relationship, a tamo je foreign key prema ovom id-u
    #orm nekako zna da moze biti many itemsa unutar jedan store i automatski je lista
    #Ako imamo puno itema, dohvat moze biti spora operacija, pa mozemo reci da je lazy=dynamic, 
    #sa tim moramo definirati dohvat tipa u def json:... items.ALL() jer item nisu rezultati nego query builder kojeg artikuliramo sa npr all()
    items = db.relationship('ItemModel', lazy='dynamic')

    def __init__(self, name, price):
        self.name = name
        self.price = price

    def json(self):
        return {'name':self.name, 'items':[item.json() for item in self.items.all()]}

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