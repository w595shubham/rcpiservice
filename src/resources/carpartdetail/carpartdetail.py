import json
import logging
import os
import sqlite3

from flask import Blueprint, make_response
from flask_restplus import Api, Resource

from src.constants import sql_object
from src.infrastructure.logging.initialize import LoggerAdapter
from src.infrastructure.security.middleware.secureroute import secureroute
from src.utilities.utilities import image_to_byte_array, save_pdf

carpartdetail_blueprint = Blueprint('carpartdetail', __name__)
api = Api(carpartdetail_blueprint, doc='/carpartdetails/docs')

ns_carpartdetails = api.namespace('carpartdetails', description='Car part detail operations')


@ns_carpartdetails.route('/<code>')
class CarPartDetails(Resource):
    @secureroute()
    def get(self, code):
        logger = logging.getLogger(__name__)
        logger = LoggerAdapter(logger)

        try:
            # Get component details by component code
            logger.info("Get component details by component code start")

            # Path to sqlite database file
            database_file = os.path.join(os.path.abspath(__file__ + "/../../../"), 'db.sqlite3')
            logger.info("Path to sqlite database file: %s", database_file)

            # Create database connection with sqlite database
            conn = sqlite3.connect(database_file)
            cursor = conn.cursor()
            fetch_query = sql_object.GET_CAR_PART_DETAILS_BY_CODE % code
            logger.info("GET_CAR_PART_DETAILS_BY_CODE query %s", fetch_query)

            # Execute query and fetch result
            cursor.execute(fetch_query)
            result_set = cursor.fetchall()

            # Prepare data to return
            items = []
            for row in result_set:
                # image_path = os.path.join(os.path.abspath(__file__ + "/../../../images"), row[4])
                # image_byte = image_to_byte_array(image_path)
                items.append({
                    'id': row[0],
                    'code': row[1],
                    'name': row[2],
                    'display_name': row[3],
                    'image': row[4],
                    'modelno': row[5],
                    'manufacturer': row[6],
                    'make': row[7],
                    'dimensions': row[8],
                    'color': row[9],
                    'price': row[10],
                    'currency': row[11],
                    # 'imagebytes': image_byte,
                })

            logger.info("Get component details by component code end")
            return json.loads(json.dumps(items)), 200, {'Content-type': 'application/json'}
        except Exception as e:
            logger.error("Fatal error in main loop", exc_info=True)
            return json.dumps(['Internal server error']), 500, {'Content-type': 'application/json'}


@ns_carpartdetails.route('/<part_id>/pdf')
class CarPartDetails(Resource):
    def get(self, part_id):
        logger = logging.getLogger(__name__)
        logger = LoggerAdapter(logger)

        try:
            # Generate PDF of component details
            logger.info("Generate PDF of component details start")

            # Path to sqlite database file
            database_file = os.path.join(os.path.abspath(__file__ + "/../../../"), 'db.sqlite3')
            logger.info("Path to sqlite database file: %s", database_file)

            # Create database connection with sqlite database
            conn = sqlite3.connect(database_file)
            cursor = conn.cursor()
            fetch_query = sql_object.GET_CAR_PART_DETAILS_BY_ID % part_id
            logger.info("GET_CAR_PART_DETAILS_BY_CODE query %s", fetch_query)

            # Execute query and fetch result
            cursor.execute(fetch_query)
            result_set = cursor.fetchall()

            # Get data for pdf creation
            items = []
            image_byte = ''
            for row in result_set:
                image_path = os.path.join(os.path.abspath(__file__ + "/../../../images"), row[1] + "_" + str(row[0]) + ".jpg")
                image_byte = image_to_byte_array(image_path)
                items.append({
                    'id': row[0],
                    'code': row[1],
                    'name': row[2],
                    'display_name': row[3],
                    'image': row[4],
                    'modelno': row[5],
                    'manufacturer': row[6],
                    'make': row[7],
                    'dimensions': row[8],
                    'color': row[9],
                    'price': row[10],
                    'currency': row[11],
                    'imagebytes': image_byte,
                })

            # Create pdf from component details and get bytes
            pdf_bytes = save_pdf(items[0], image_byte)

            # Prepare data to return
            response = make_response(pdf_bytes)
            response.headers.set('Content-Type', 'application/pdf')
            response.headers.set(
                'Content-Disposition', 'attachment', filename='%s.pdf' % items[0]['code'])
            return response
        except Exception as e:
            logger.error("Fatal error in main loop", exc_info=True)
            return json.dumps(['Internal server error']), 500, {'Content-type': 'application/json'}

