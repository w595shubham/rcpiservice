from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from src import db


class CarPartRelationshipHierarchy(db.Model):
    __tablename__ = 'carpartrelationshiphierarchy'
    id = db.Column(db.Integer, primary_key=True)
    parent_category_id = Column(Integer, ForeignKey('carpartcategory.id'))
    child_category_id = Column(Integer, ForeignKey('carpartcategory.id'))

