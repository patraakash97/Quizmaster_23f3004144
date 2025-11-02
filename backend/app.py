from flask import Flask
from application.models import db, User, Role, UserRoles
from flask_security import Security, SQLAlchemyUserDatastore
from application.config import localDatabaseConfig


def create_app():
    app = Flask(__name__,template_folder="../frontend_cdn/",static_folder="../frontend_cdn/")
    app.config.from_object(localDatabaseConfig)
    db.init_app(app)
    datastore= SQLAlchemyUserDatastore(db, User, Role)
    app.security = Security(app,datastore=datastore,register_blueprint=False)
    app.app_context().push()
    return app

app=create_app()

from application.initial_data import *
from application.routes import *

if __name__ == '__main__':
    app.run(debug=True)