from src import db


class CarPartCategory(db.Model):
    __tablename__ = 'carpartcategory'
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(100))
    display_name = db.Column(db.String(500))
    image = db.Column(db.String(1000))
