from flask import current_app as app
from .models import db
from flask_security import Security, SQLAlchemyUserDatastore
from flask_security import hash_password

with app.app_context():
    db.create_all()

    datastore=app.security.datastore

    if not datastore.find_role("admin"):
        datastore.create_role(name="admin", description="superuser")
    if not datastore.find_role("doctor"):
        datastore.create_role(name="doctor", description="doctor")
    if not datastore.find_role("patient"):
        datastore.create_role(name="patient", description="patient")

    if (not datastore.find_user(email="admin@example.com")):
        datastore.create_user(name="admin", email="admin@example.com", password=hash_password("password"), roles=["admin"])
    if (not datastore.find_user(email="doctor1@example.com")):
        datastore.create_user(name="doctor1", email="doctor1@example.com", password=hash_password("password"), roles=["doctor"])
    if (not datastore.find_user(email="patient1@example.com")):
        datastore.create_user(name="patient1", email="patient1@example.com", password=hash_password("password"), roles=["patient"])

    db.session.commit()
    print("Initial data created successfully.")