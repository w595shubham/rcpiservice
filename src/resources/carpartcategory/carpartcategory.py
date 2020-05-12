import json
import logging
import os
import sqlite3

import requests
from flask import Blueprint, request
from flask_restplus import Api, Resource
from werkzeug.datastructures import FileStorage

from src.constants import sql_object
from src.infrastructure.logging.initialize import LoggerAdapter
from src.infrastructure.security.middleware.secureroute import secureroute
from src.utilities.utilities import image_to_byte_array

carpartcategory_blueprint = Blueprint('carpartcategory', __name__)
api = Api(carpartcategory_blueprint, doc='/carpartcategories/docs')
ns_carpartcategories = api.namespace('carpartcategories', description='Car part detail operations')

upload_parser = api.parser()
upload_parser.add_argument('file', location='files', type=FileStorage, required=True)


@ns_carpartcategories.route('/')
class CarPartCategoryList(Resource):
    @secureroute()
    def get(self):
        logger = logging.getLogger(__name__)
        logger = LoggerAdapter(logger)

        try:
            # Get component details by component code
            logger.info("Get component categories by component code start")

            # Path to sqlite database file
            database_file = os.path.join(os.path.abspath(__file__ + "/../../../"), 'db.sqlite3')
            logger.info("Path to sqlite database file: %s", database_file)

            # Create database connection with sqlite database
            conn = sqlite3.connect(database_file)
            cursor = conn.cursor()
            fetch_query = sql_object.GET_CAR_PART_CATEGORIES
            logger.info("GET_CAR_PART_CATEGORIES query %s", fetch_query)

            # Execute query and fetch result
            cursor.execute(fetch_query)
            result_set = cursor.fetchall()

            # Prepare data to return
            items = []
            for row in result_set:
                items.append({
                    'id': row[0],
                    'code': row[1],
                    'name': row[2],
                    'display_name': row[3],
                })

            logger.info("Get component categories by component code end")
            return json.loads(json.dumps(items)), 200, {'Content-type': 'application/json'}
        except Exception as e:
            logger.error("Fatal error in main loop", exc_info=True)
            return json.dumps(['Internal server error']), 500, {'Content-type': 'application/json'}

    @secureroute()
    def post(self):
        logger = logging.getLogger(__name__)
        logger = LoggerAdapter(logger)
        logger.info('File upload started')
        categories = ['E & F Knuckles', 'Chock track', 'Coil Covers', 'Door Frames']
        # check if the post request has the file part
        try:
            args = upload_parser.parse_args()
            uploaded_file = args['file']  # This is FileStorage instance
            token = request.headers.get("authorization", None)

            # Make request to image prediction api
            response = requests.post('http://35.239.91.46:5000/objectdetection/',
                                     files={'file': uploaded_file},
                                     headers={'Authorization': token,
                                              'Access-Control-Allow-Origin': '*',
                                              'Access-Control-Allow-Credentials': 'true', })

            if response.ok:
                detected_parts = list(set(map(lambda x: x['part'], json.loads(response.text)['predictions'])))
                predicted_image_byte = json.loads(response.text)['imagebytes']
                # Path to sqlite database file
                database_file = os.path.join(os.path.abspath(__file__ + "/../../../"), 'db.sqlite3')
                logger.info("Path to sqlite database file: %s", database_file)

                # Create database connection with sqlite database
                conn = sqlite3.connect(database_file)
                cursor = conn.cursor()
                category_list = ', '.join('"{0}"'.format(o) for o in detected_parts)
                fetch_query = sql_object.GET_CAR_PART_DETAILS_BY_CATEGORIES % category_list
                logger.info("GET_CAR_PART_CATEGORIES_BY_KEYWORD query %s", fetch_query)

                # Execute query and fetch result
                cursor.execute(fetch_query)
                result_set = cursor.fetchall()

                # Prepare data to return
                items = []
                for row in result_set:
                    items.append({
                        'id': row[0],
                        'code': row[1],
                        'name': row[2],
                        'display_name': row[3],
                        'image': row[4],
                        'subcategories': row[5],
                        'variations': row[6],
                        'predictedImage': predicted_image_byte
                    })

                logger.info("Get component categories by component code end")
                return json.loads(json.dumps(items)), 200, {'Content-type': 'application/json'}
        except Exception as e:
            logger.error("Fatal error in main loop", exc_info=True)
        return json.dumps(['Internal server error']), 500, {'Content-type': 'application/json'}


class Prediction:
    def __init__(self, category, probability):
        self.category = category
        self.probability = probability


# def load_image(img_path):
#     img = image.load_img(img_path, target_size=(224, 224))
#     img_tensor = image.img_to_array(img)
#     img_tensor = np.expand_dims(img_tensor, axis=0)
#     return img_tensor


@ns_carpartcategories.route('/<code>')
class CarPartCategoryByCode(Resource):
    @secureroute()
    def get(self, code):
        logger = logging.getLogger(__name__)
        logger = LoggerAdapter(logger)

        try:
            # Get component details by component code
            logger.info("Get component categories by component code start")

            # Path to sqlite database file
            database_file = os.path.join(os.path.abspath(__file__ + "/../../../"), 'db.sqlite3')
            logger.info("Path to sqlite database file: %s", database_file)

            # Create database connection with sqlite database
            conn = sqlite3.connect(database_file)
            cursor = conn.cursor()
            fetch_query = sql_object.GET_CAR_PART_CATEGORIES_BY_CODE % code
            logger.info("GET_CAR_PART_CATEGORIES_BY_CODE query %s", fetch_query)

            # Execute query and fetch result
            cursor.execute(fetch_query)
            result_set = cursor.fetchall()

            # Prepare data to return
            items = []
            for row in result_set:
                items.append({
                    'id': row[0],
                    'code': row[1],
                    'name': row[2],
                    'display_name': row[3],
                })

            logger.info("Get component categories by component code end")
            return json.loads(json.dumps(items)), 200, {'Content-type': 'application/json'}
        except Exception as e:
            logger.error("Fatal error in main loop", exc_info=True)
            return json.dumps(['Internal server error']), 500, {'Content-type': 'application/json'}


@ns_carpartcategories.route('/search/<keyword>')
class CarPartCategoryByKeyword(Resource):
    @secureroute()
    def get(self, keyword):
        logger = logging.getLogger(__name__)
        logger = LoggerAdapter(logger)

        try:
            # Get component details by component code
            logger.info("Get component categories by component code start")

            # Path to sqlite database file
            database_file = os.path.join(os.path.abspath(__file__ + "/../../../"), 'db.sqlite3')
            logger.info("Path to sqlite database file: %s", database_file)

            # Create database connection with sqlite database
            conn = sqlite3.connect(database_file)
            cursor = conn.cursor()
            fetch_query = sql_object.GET_CAR_PART_CATEGORIES_BY_KEYWORD % keyword
            logger.info("GET_CAR_PART_CATEGORIES_BY_KEYWORD query %s", fetch_query)

            # Execute query and fetch result
            cursor.execute(fetch_query)
            result_set = cursor.fetchall()

            # Prepare data to return
            items = []
            for row in result_set:
                items.append({
                    'id': row[0],
                    'code': row[1],
                    'name': row[2],
                    'display_name': row[3],
                    'image': row[4],
                    'subcategories': row[5],
                    'variations': row[6]
                })

            logger.info("Get component categories by component code end")
            return json.loads(json.dumps(items)), 200, {'Content-type': 'application/json'}
        except Exception as e:
            logger.error("Fatal error in main loop", exc_info=True)
            return json.dumps(['Internal server error']), 500, {'Content-type': 'application/json'}


@ns_carpartcategories.route('/major')
class CarPartMajorCategoryList(Resource):
    @secureroute()
    def get(self):
        logger = logging.getLogger(__name__)
        logger = LoggerAdapter(logger)

        try:
            # Get component details by component code
            logger.info("Get major component categories by component code start")

            # Path to sqlite database file
            database_file = os.path.join(os.path.abspath(__file__ + "/../../../"), 'db.sqlite3')
            logger.info("Path to sqlite database file: %s", database_file)

            # Create database connection with sqlite database
            conn = sqlite3.connect(database_file)
            cursor = conn.cursor()
            fetch_query = sql_object.GET_CAR_PART_MAJOR_CATEGORIES
            logger.info("GET_CAR_PART_MAJOR_CATEGORIES_BY_CODE query %s", fetch_query)

            # Execute query and fetch result
            cursor.execute(fetch_query)
            result_set = cursor.fetchall()

            # Prepare data to return
            items = []
            for row in result_set:
                items.append({
                    'id': row[0],
                    'code': row[1],
                    'name': row[2],
                    'display_name': row[3],
                    'image': row[4],
                    'subcategories': row[5],
                    'variations': row[6]
                })

            logger.info("Get major component categories by component code end")
            return json.loads(json.dumps(items)), 200, {'Content-type': 'application/json'}
        except Exception as e:
            logger.error("Fatal error in main loop", exc_info=True)
            return json.dumps(['Internal server error']), 500, {'Content-type': 'application/json'}


@ns_carpartcategories.route('/<name>/image')
class CarPartCategoryImageByName(Resource):
    def get(self, name):
        logger = logging.getLogger(__name__)
        logger = LoggerAdapter(logger)

        try:
            # Getting image for car part
            logger.info("Getting image for car part: " + name)
            image_path = os.path.join(os.path.abspath(__file__ + "/../../../images"), name + ".jpg")
            logger.info("Image path: " + image_path)
            image_byte = image_to_byte_array(image_path)

            # Prepare data for image bytes to return
            returnData = {
                'imagebytes': image_byte,
            }

            return json.loads(json.dumps(returnData)), 200, {'Content-type': 'application/json'}
        except Exception as e:
            logger.error("Fatal error in main loop", exc_info=True)
            return json.dumps(['Internal server error']), 500, {'Content-type': 'application/json'}
