from flask import Flask
from application.models import db, User, Role, UserRoles
from flask_security import Security, SQLAlchemyUserDatastore
from application.config import localDatabaseConfig
from flask_cors import CORS
from application.api import api



def create_app():
    app = Flask(__name__,template_folder="../frontend_cdn/",static_folder="../frontend_cdn/")
    app.config.from_object(localDatabaseConfig)
    db.init_app(app)
    api.init_app(app)
    CORS(app)
    
    datastore= SQLAlchemyUserDatastore(db, User, Role)
    app.security = Security(app,datastore=datastore,register_blueprint=False)
    @app.security.unauthn_handler
    def unauthn_handler(reason,headers=None):
        return {"message": f"please provide {reason[0]}"}, 401
    

    @app.security.unauthn_handler
    def unauthz_handler(func_name,params):
        return {"message": f"you are not authorized to access {params[0]} resource"}, 403
    app.app_context().push()
    return app

app=create_app()

from application.initial_data import *
from application.routes import *

if __name__ == '__main__':
    app.run(debug=True)