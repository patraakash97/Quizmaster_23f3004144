from flask import current_app as app
from .models import db,Subject,Chapter, Role
from flask_security import SQLAlchemyUserDatastore
from flask_security import hash_password

with app.app_context():
    db.create_all()
    
    datastore = app.security.datastore


    
    if not datastore.find_role("admin"):
        datastore.create_role(name="admin", description="superuser")
    if not datastore.find_role("student"):
        datastore.create_role(name="student", description="student")
    
    

    if (not datastore.find_user(email = "admin@gmail.com")):
        datastore.create_user(name ="admin" , email = 'admin@gmail.com', password = hash_password('pass'), roles = ['admin'] )
    if (not datastore.find_user(email = 'stud1@gmail.com')):
        datastore.create_user(name="stud1" ,email = 'stud1@gmail.com', password = hash_password('pass'), roles = ['student'] )
    
    db.session.commit()
    if Subject.query.count() == 0:
        subjects = [
            Subject(sub_name="Mathematics", sub_desc="All about numbers and equations"),
            Subject(sub_name="Science", sub_desc="Explore the world of science"),
            Subject(sub_name="History", sub_desc="Learn about historical events"),
            Subject(sub_name="Geography", sub_desc="Study the Earth's landscapes"),
            Subject(sub_name="Literature", sub_desc="Dive into classic and modern texts")
        ]
        db.session.bulk_save_objects(subjects)
    
        db.session.commit()
    if Chapter.query.count() == 0:
        chapters = [
            Chapter(ch_name="Integers", ch_desc="All about integer numbers" , sub_id=1),
            Chapter(ch_name="Real Numbers", ch_desc="All about Real numbers", sub_id=1),
            
        ]
        db.session.bulk_save_objects(chapters)
    
        db.session.commit()
    
    print("Initial data created")
    