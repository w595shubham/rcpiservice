import logging
from configparser import SafeConfigParser

from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash

from src.infrastructure.logging.initialize import setup_logging

db = SQLAlchemy()

config = SafeConfigParser()
config.read('config.ini')

app = Flask(__name__)
CORS(app)

app.config['SECRET_KEY'] = config.get('app', 'SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = config.get('db', 'SQLALCHEMY_DATABASE_URI')
app.config['USERNAME'] = config.get('app', 'USERNAME')
app.config['PASSWORD'] = generate_password_hash(config.get('app', 'PASSWORD'), method='sha256')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialise database
db.init_app(app)

# Initialise logging
setup_logging()
logger = logging.getLogger(__name__)


def get_app():
    from src.models.carpartcategory import CarPartCategory
    from src.models.carpartrelationshiphierarchy import CarPartRelationshipHierarchy
    from src.models.carpartdetail import CarPartDetail
    return app