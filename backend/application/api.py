from flask_restful import Resource, Api,request
api = Api()
from .models import *
from flask_security import auth_required,roles_required

from .task import Quiz_alert
class SubjectsAPI(Resource):
    @auth_required('token')
    def get(self):
        subjects = Subject.query.all()
        subs = []
        for sub in subjects:
            subs.append({"name" : sub.sub_name , "description" : sub.sub_desc , "id":sub.sub_id})
        
        return subs,200
    
    def post(self):
        formdata= request.get_json()
        try:
            sub = Subject.query.filter_by(sub_name=formdata.get("name")).first()
            if sub:
                return {"message" :"Subject already exist"} , 409
            else:
                new_sub = Subject(sub_name = formdata.get("name") , sub_desc = formdata.get("description"))
                db.session.add(new_sub)
                db.session.commit()
            
                return {"id": new_sub.sub_id , "name" : new_sub.sub_name , "desc" : new_sub.sub_desc} ,200
        
        except Exception as e:
            print(e)
            db.session.rollback()
            return {"message" : "internal server error"} , 500
            
        
    def put(self):
        id = request.args.get("id")
        formdata= request.get_json()
        try:
            sub = Subject.query.filter_by(sub_id = id).first()

            if sub:
                if formdata.get("name"):
                    if not  Subject.query.filter(Subject.sub_name.ilike( f"%{formdata.get("name")}%" )).first():
                        sub.sub_name = formdata.get("name")
                    else:
                        return {"message" :"Subject already exist"} , 409
                if formdata.get("description"):
                    sub.sub_desc = formdata.get("description")
                db.session.commit()
                return {"message" :"Subject is updated"} , 200
            else:
                return {"message" :"Subject doesn't exist"} , 404
        
        except Exception as e:
            print(e)
            db.session.rollback()
            return {"message" : "internal server error"} , 500
            
        

    def delete(self):
        id = request.args.get("id")
        try:
            sub = Subject.query.filter_by(sub_id = id).first()
            if sub:
                db.session.delete(sub)
                db.session.commit()
                return {"message" : "subject is deleted"} , 200
            else:
                return {"message" : "subject doesn't exist"} , 404
        except Exception as e :
            print(e)
            db.session.rollback()
            return {"message" : "internal server error"} , 500
        
class ChaptersAPI(Resource):
    def get(self):
        if request.args.get("sub_name"):
            try:
                sub = Subject.query.filter_by(sub_name = request.args.get("sub_name")).first()

                chapters = Chapter.query.filter_by(sub_id = sub.sub_id ).all()
                L = []
                for chap in chapters:
                    L.append({"id" : chap.ch_id , "name" : chap.ch_name , "description" : chap.ch_desc})
                return L, 200
            except Exception as e:
                print(e)
                db.session.rollback()
                return {"message" :"internal server error" } , 500
        else : 
            try:
                chapters = Chapter.query.all()
                L = []
                for chap in chapters:
                    L.append({"id" : chap.ch_id , "name" : chap.ch_name , "description" : chap.ch_desc})
                    return L, 200
            except Exception as e:
                print(e)
                db.session.rollback()
                return {"message" :"internal server error" } , 500
            
    def post(self):
        
        formdata= request.get_json()
        try:
            chap = Chapter.query.filter_by(ch_name=formdata.get("name")).first()
            if chap:
                return {"message" :"chapter already exist"} , 409
            else:
                sub = Subject.query.filter_by(sub_name = request.args.get("sub_name")).first()
                new_sub = Chapter(ch_name = formdata.get("name") , ch_desc = formdata.get("description") , sub_id = sub.sub_id)
                db.session.add(new_sub)
                db.session.commit()
            
                return {"message" :"chapter Created successfully"} ,200
        
        except Exception as e:
            print(e)
            db.session.rollback()
            return {"message" : "internal server error"} , 500
    
    def delete(self):
        id = request.args.get("ch_id")
        try:
            ch = Chapter.query.filter_by(ch_id = id).first()
            if ch:
                db.session.delete(ch)
                db.session.commit()
                return {"message" : "Chapter is deleted"} , 200
            else:
                return {"message" : "Chapter doesn't exist"} , 404
        except Exception as e :
            print(e)
            db.session.rollback()
            return {"message" : "internal server error"} , 500


class QuizResource(Resource):
    def get(self):
        if request.args.get("id"):
            quiz = Quiz.query.filter_by(quiz_id =request.args.get("id")).first()
            if not quiz:
                return {"message" :"quiz not found"} , 404
            qz= {}
            qz["name"] = quiz.quiz_name

            qz["total_marks"] = quiz.total_marks
            qz["questions"] = []
            for question in quiz.questions:
                qz["questions"].append({"statement" : question.question_statement ,
                                         "marks": question.marks ,
                                           "A": question.option1 ,
                                           "B": question.option2 ,
                                            "C" : question.option3,
                                            "D" : question.option4 , 
                                            })
            return qz, 200


        else:
            ch_name = request.args.get("ch_name")
            if not ch_name :
                return {"message": "provide the chapter name"}, 404
            chapter = Chapter.query.filter_by(ch_name = ch_name).first()
            if not chapter:
                return {"message": "chapter doesn't exist"}, 404
            
            quizes = chapter.quizes
            q_list = []
            for q in quizes:
                q_list.append({"id" : q.quiz_id , "name" : q.quiz_name , 'date' : q.quiz_date , 'total_marks' : q.total_marks})
            return q_list , 200


    def post(self):

        data = request.get_json()
        ch_name= request.args.get("ch_name")
        if not data:
            return {'message': 'No JSON payload received'}, 400

        try:
            chapter = Chapter.query.filter_by(ch_name=ch_name).first()
            if not chapter:
                return {'message': f"Chapter '{ch_name}' not found"}, 404
            
        
            total_marks = 0
            new_quiz = Quiz(
                quiz_name=data.get('quiz_name'),
                quiz_date=data.get('quiz_date'),
                ch_id=chapter.ch_id
            )
            db.session.add(new_quiz)
            db.session.commit()
            questions_data = data.get('questions', [])
            
            for q in questions_data:
                
                question_marks = int(q['marks'])
                total_marks += question_marks
            

                new_question = Questions(
                    question_statement=q.get('statement'),
                    option1=q.get('A'),
                    option2=q.get('B'),
                    option3=q.get('C'),
                    option4=q.get('D'),
                    answer=q.get('correct'),
                    marks=question_marks,
                    quiz_id= new_quiz.quiz_id
                )
                db.session.add(new_question)
                db.session.commit()

            new_quiz.total_marks = total_marks
            
            db.session.commit()
            Quiz_alert.delay(new_quiz.quiz_id)
            return {'message': 'Quiz created successfully', 'quiz_id': new_quiz.quiz_id}, 200
        except Exception as e:
            db.session.rollback()
            return {'message': f'An error occurred while creating the quiz {e}',}, 500           




api.add_resource(SubjectsAPI, '/api/subjects')
api.add_resource(ChaptersAPI, '/api/chapters')
api.add_resource(QuizResource , "/api/quizes")
        