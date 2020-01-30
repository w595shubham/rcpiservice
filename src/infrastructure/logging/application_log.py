import os
from src.infrastructure.security.middleware.secureroute import secureroute
from flask import Blueprint, safe_join, send_file, abort
from flask_restplus import Api, Resource

application_log_blueprint = Blueprint('application_log', __name__)
api = Api(application_log_blueprint, doc='/applicationlog/docs')
ns_applicationlog = api.namespace('applicationlog', description='Car part detail operations')


@ns_applicationlog.route('/<log_file>')
class ApplicationLog(Resource):
    @secureroute()
    def get(self, log_file):
        safe_path = safe_join(os.path.abspath(__file__ + "/../../../../logs"), log_file)

        try:
            return send_file(safe_path, as_attachment=True)
        except FileNotFoundError:
            abort(404)
