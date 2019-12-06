#from sqlalchemy.dialects.postgresql import JSON
from app import db
from sqlalchemy.dialects.postgresql import JSON





class Hotel(db.Model):
    __tablename__ = 'hotels'

    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String())
    start_date = db.Column(db.Date)
    final_date = db.Column(db.Date)
    price = db.Column(db.String(16))
    alternative = db.Column(db.JSON())

    #alternative = db.column(JSON)

    def __init__(self,name,start_date,final_date,price,alternative):
        self.name = name
        self.start_date = start_date
        self.final_date = final_date
        self.price = price
        self.alternative = alternative

    def __repr__(self):
        return f'name = {self.name}'
    
    def to_json(self):
        return {
            'name':self.name,
            'start_date':self.start_date,
            'final_date':self.final_date,
            'price':self.price,
            'alternative':self.alternative
        }