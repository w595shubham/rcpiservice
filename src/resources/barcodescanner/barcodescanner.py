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

barcodedetection_blueprint = Blueprint('decodebarcode', __name__)
api = Api(barcodedetection_blueprint, doc='/decodebarcode/docs')
ns_barcodedetection = api.namespace('decodebarcode', description='Bar Code Detection')

upload_parser = api.parser()
upload_parser.add_argument('file', location='files', type=FileStorage, required=True)


@ns_barcodedetection.route('/')
class BarCodeDetection(Resource):
    @secureroute()
    def post(self):
        logger = logging.getLogger(__name__)
        logger = LoggerAdapter(logger)
        logger.info('File upload started')
        try:
            args = upload_parser.parse_args()
            uploaded_file = args['file']  # This is FileStorage instance
            token = request.headers.get("authorization", None)

            response = requests.post('http://35.239.91.46:5000/objectdetection/decodebarcode',
                                     files={'file': uploaded_file},
                                     headers={'Authorization': token,
                                              'Access-Control-Allow-Origin': '*',
                                              'Access-Control-Allow-Credentials': 'true', })

            if response.ok and response.text.__len__() > 0:
                barcode_list = ', '.join('"{0}"'.format(o.strip()) for o in json.loads(response.text))

                # Path to sqlite database file
                database_file = os.path.join(os.path.abspath(__file__ + "/../../../"), 'db.sqlite3')
                logger.info("Path to sqlite database file: %s", database_file)

                # Create database connection with sqlite database
                conn = sqlite3.connect(database_file)
                cursor = conn.cursor()
                fetch_query = sql_object.GET_CAR_PART_DETAILS_BY_BARCODE % barcode_list
                logger.info("GET_CAR_PART_DETAILS_BY_BARCODE query %s", fetch_query)

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

