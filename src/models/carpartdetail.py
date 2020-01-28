from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from src import db


class CarPartDetail(db.Model):
    __tablename__ = 'carpartdetail'
    id = db.Column(db.Integer, primary_key=True)
    category_id = Column(Integer, ForeignKey('carpartcategory.id'))
    modelno = db.Column(db.String(100))
    manufacturer = db.Column(db.String(100))
    make = db.Column(db.String(100))
    dimensions = db.Column(db.String(100))
    color = db.Column(db.String(100))
    price = db.Column(db.String(100))
    currency = db.Column(db.String(100))
