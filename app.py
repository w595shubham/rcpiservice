from src import app
from src.infrastructure.logging.application_log import application_log_blueprint
from src.infrastructure.security.authentication.token import mod as token
from src.resources.carpartcategory.carpartcategory import carpartcategory_blueprint
from src.resources.carpartdetail.carpartdetail import carpartdetail_blueprint
from src.resources.carpartrelationshiphierarchy.carpartrelationshiphierarchy import carpartrelationshiphierarchy_blueprint

app.register_blueprint(carpartcategory_blueprint)
app.register_blueprint(carpartdetail_blueprint)
app.register_blueprint(carpartrelationshiphierarchy_blueprint)
app.register_blueprint(token)
app.register_blueprint(application_log_blueprint)

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)
