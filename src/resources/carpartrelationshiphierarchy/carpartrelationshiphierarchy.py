import json
import logging
import os
import sqlite3

from flask import Blueprint
from flask_restplus import Api, Resource

from src.constants import sql_object
from src.infrastructure.logging.initialize import LoggerAdapter
from src.infrastructure.security.middleware.secureroute import secureroute

carpartrelationshiphierarchy_blueprint = Blueprint('carpartrelationshiphierarchy', __name__)
api = Api(carpartrelationshiphierarchy_blueprint, doc='/carpartrelationshiphierarchies/docs')

ns_carpartrelationshiphierarchies = api.namespace('carpartrelationshiphierarchies', description='Car part detail operations')


@ns_carpartrelationshiphierarchies.route('/<code>')
class CarPartRelationshipHierarchies(Resource):
    @secureroute()
    def get(self, code):
        logger = logging.getLogger(__name__)
        logger = LoggerAdapter(logger)

        try:
            # Get component relationship hierarchy by component code
            logger.info("Get component relationship hierarchy by component code start")

            # Path to sqlite database file
            database_file = os.path.join(os.path.abspath(__file__ + "/../../../"), 'db.sqlite3')
            logger.info("Path to sqlite database file: %s", database_file)

            # Create database connection with sqlite database
            conn = sqlite3.connect(database_file)
            cursor = conn.cursor()
            fetch_query = sql_object.GET_CAR_PART_SUB_CATEGORIES_BY_CODE % code
            logger.info("GET_CAR_PART_RELATIONSHIPHIERARCHIES_BY_CODE query %s", fetch_query)

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

            logger.info("Get component relationship hierarchy by component code end")
            return json.loads(json.dumps(items)), 200, {'Content-type': 'application/json'}
        except Exception as e:
            logger.error("Fatal error in main loop", exc_info=True)
            return json.dumps(['Internal server error']), 500, {'Content-type': 'application/json'}



