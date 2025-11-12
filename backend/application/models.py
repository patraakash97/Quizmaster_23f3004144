from flask_sqlalchemy import SQLAlchemy
from flask_security import UserMixin, RoleMixin
from sqlalchemy.types import JSON

db=SQLAlchemy()


class User(db.Model,UserMixin):
    __tablename__='user'
    id=db.Column(db.Integer, primary_key=True, autoincrement= True)
    name=db.Column(db.String,nullable = False)
    email=db.Column(db.String,unique=True, nullable = False)
    password=db.Column(db.String,unique=True, nullable = False)
    user_qualification=db.Column(db.String)
    user_dob=db.Column(db.String,unique=True)
    active = db.Column(db.Boolean, default=True)
    fs_uniquifier = db.Column(db.String,unique=True, nullable = False)
    roles = db.relationship("Role",backref="bearers", secondary = "user_roles")
    scores =db.relationship("Scores",backref="user", cascade='all, delete-orphan')

class Role(db.Model,RoleMixin):
    role_id = db.Column(db.Integer, primary_key=True, autoincrement= True) 
    name=db.Column(db.String, unique=True, nullable = False)
    description = db.Column(db.String)


class UserRoles(db.Model):
    ur_id = db.Column(db.Integer, primary_key=True, autoincrement= True)
    role_id = db.Column(db.Integer, db.ForeignKey("role.role_id"))
    user_id=db.Column(db.Integer, db.ForeignKey("user.id"),nullable = False)

class Subject(db.Model):
    __tablename__='subject'
    sub_id = db.Column(db.Integer, primary_key=True, autoincrement= True)
    sub_name = db.Column(db.String, unique = True, nullable = False)
    sub_desc = db.Column(db.String)
    chapters =db.relationship("Chapter",backref="subject",cascade='all, delete-orphan')
    scores = db.relationship("Scores",backref="subject", cascade='all, delete-orphan')

class Chapter(db.Model):
    __tablename__='chapter'
    ch_id = db.Column(db.Integer, primary_key=True, autoincrement= True)
    ch_name = db.Column(db.String,unique = True, nullable = False)
    ch_desc = db.Column(db.String)
    sub_id = db.Column(db.Integer, db.ForeignKey("subject.sub_id"), nullable = False)
    quizes =db.relationship("Quiz",backref="chapter", cascade='all, delete-orphan')
    


class Quiz(db.Model):
    __tablename__ = 'quiz'
    quiz_id= db.Column(db.Integer, primary_key=True, autoincrement= True)
    ch_id = db.Column(db.Integer, db.ForeignKey("chapter.ch_id"))
    quiz_date = db.Column(db.String)
    quiz_duration = db.Column(db.String)
    quiz_remarks = db.Column(db.String)
    quiz_name = db.Column(db.String, nullable = False)
    questions =db.relationship("Questions",backref="quiz", cascade='all, delete-orphan')
    scores =db.relationship("Scores",backref="quiz", cascade='all, delete-orphan')
    total_marks = db.Column(db.Integer)
    

class Questions(db.Model):
    __tablename__='questions'
    ques_id= db.Column(db.Integer, primary_key=True, autoincrement= True)
    quiz_id = db.Column(db.Integer, db.ForeignKey("quiz.quiz_id"))
    question_statement =  db.Column(db.String) 
    option1 = db.Column(db.String)
    option2 = db.Column(db.String)
    option3 = db.Column(db.String)
    option4 = db.Column(db.String)
    answer = db.Column(db.String)
    marks = db.Column(db.Integer)

class Scores(db.Model):
    __tablename__='scores'
    score_id = db.Column(db.Integer, primary_key=True, autoincrement= True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    quiz_id = db.Column(db.Integer, db.ForeignKey("quiz.quiz_id"))
    sub_id = db.Column(db.Integer, db.ForeignKey("subject.sub_id"))
    TimeStamp_attempt = db.Column(db.String)
    total_scored = db.Column(db.Integer)
    resp = db.Column(JSON)