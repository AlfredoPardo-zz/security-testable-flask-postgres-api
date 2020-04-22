from flask import Flask
from flask_jwt_extended import JWTManager
from database import db, reset_database
from api import api
import yaml

# APIs Import
from api.cloud.cloud_accounts import api as cloud_accounts_ns
from api.cloud.cloud_providers import api as cloud_providers_ns
from api.general.customers import api as customers_ns
from api.general.users import api as users_ns

app = Flask(__name__)

def configure_app(flask_app):

    with open("config.yaml") as f:
    
        config = yaml.load(f, Loader=yaml.FullLoader)

    DB_URL = 'postgresql+psycopg2://{}:{}@{}/{}'.\
        format(config["postgres"]["username"], \
        config["postgres"]["password"], \
        config["postgres"]["host"],
        config["postgres"]["database"])

    flask_app.config['JWT_SECRET_KEY'] = config["jwt"]["secret_key"]
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    return config["initialize_db"]

def initialize_app(app):
    
    initialize_db = configure_app(app)

    api.add_namespace(cloud_accounts_ns)
    api.add_namespace(cloud_providers_ns)
    api.add_namespace(customers_ns)
    api.add_namespace(users_ns)
    api.init_app(app)
    db.init_app(app)
    jwt = JWTManager(app)

    if initialize_db:
        reset_database(app)

initialize_app(app)

if __name__ == "__main__":
    app.run(debug=True)

