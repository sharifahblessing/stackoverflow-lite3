import datetime
from flask import Flask, jsonify, make_response
from werkzeug.security import generate_password_hash, \
    check_password_hash
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity,create_refresh_token
)

from flask_restful import Resource, Api, reqparse
from datetime import datetime, timedelta
from app.models import User_model, Question_model, Answer_model
from app.database import Database
import json

questions_list=[]
answers_list=[]
db = Database()

class UserSignup(Resource):
    def post(self):
        parser= reqparse.RequestParser()

        """collecting arguments"""
        
        
        parser.add_argument('name',type=str,required=True)
        parser.add_argument('username',type=str,required=True)
        parser.add_argument('password',type=str,required=True)
        
        
        """getting specific arguments"""

        argument = parser.parse_args()

    
        name = str(argument['name']).strip()
        username = str(argument['username']).strip()
        password = generate_password_hash(str(argument['password']).strip())
        
        # Query the database to check if user exits
        check_user = db.get_by_parameter('userstable','username',username)
        if not check_user :
        
            """insert into the database"""
            db.insert_user_data(name,username,password)


            return make_response(jsonify(
                {
                'message':'Registration successfull'           
            }
            ),201)
        return make_response(jsonify(
                {
                "message":"{} is already taken".format(username)           
            }
            ),409)
class UserLogin(Resource):
    """Method for login"""
    def post(self):
        """Getting data from the URL body """
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, required=True)
        parser.add_argument('password', type=str, required=True)

        argument = parser.parse_args()
        username = str(argument['username']).strip()
        password = str(argument['password']).strip()


       # if username == "" or len(username) < 3:
        #    return make_response(jsonify({"message": "invalid username, Enter correct username please"}),
                            # 400)

        #if password == "" or password == " " or len(password) < 3:
           # return make_response(jsonify({"message": "Password should be morethan 3 characters"}),
                             #400)

        query_user = db.get_by_parameter('userstable','username',username)
        print(query_user)
        if  query_user:
            
            user_obj = User_model(query_user[0],query_user[1],query_user[2],query_user[3])
            print(user_obj)
            print(check_password_hash(user_obj.password, password))
                    
            if  check_password_hash(user_obj.password, password):
                access_token = create_access_token(identity=query_user[0],fresh=True)
                
                return make_response(jsonify({"message": "Login successful",
                                            "accesstoken": access_token,
                                            
                                             }),200)
        return make_response(jsonify({"message": "User does not exist please signup first"}),
                             404)

class Questions (Resource):
    """"method for posting a question"""
    @jwt_required
    def post(self):
        parser= reqparse.RequestParser()

        """collecting arguments"""
        parser.add_argument('title',required=True)
        parser.add_argument('body',type=str,required=True)
        parser.add_argument('tag',type=str,required=True)
        

        """getting specific arguments"""

        argument = parser.parse_args()

        title = str(argument['title']).strip()
        body = argument['body']
        tag = argument['tag']

       
        # if not access_token:
        #     return make_response(jsonify({
        #         'message':'token missing'
        #     }),400)

                                        
        """Query database to check whether question exits"""
        check_question = db.get_by_parameter('questionstable','title',title)
        if  check_question:
             return make_response(jsonify(
            {
            'message':'This question already exists'}
            ),409)
        
        """checking whether the empty title feild"""
        if  not title:
            return make_response(jsonify(
        {
            'message':'The title is needed for this question to be posted'  
                }
            ),400)
        """checking whether the empty body feild"""
        if  not body:
            return make_response(jsonify(
        {
            'message':'Body is needed for this question to be posted'  
                }
            ),400)
        """checking whether the empty tag feild"""
        if  not tag:
            return make_response(jsonify(
        {
            'message':'Tag is needed for this question to be posted'  
                }
            ),400)
        """ implementing token decoding"""
        current_user = get_jwt_identity()

        """insert into the database"""
        db.insert_question_data(current_user, title,body,tag)
       
        return make_response(jsonify(
                {
                'message':'Question created successfully'}
                
            ),201)
        
       
    def get(self):
        db_questions = db.get_all('questionstable')
        
        questions_list =[]
        for question in db_questions:
            question_dict = dict()
            question_dict["question_id"] = question[0]
            question_dict["user_id"]=question[1]
            question_dict["title"]=question[2]
            question_dict["body"]=str(question[3])
            question_dict["tag"]=str(question[5])
            question_dict["posted at"]=str(question[4]) 
            questions_list.append(question_dict)

        return questions_list,200


class SingleQuestion(Resource):
    
    def get(self,questionId):
        
        question_data = db.get_by_parameter('questionstable','questionid',questionId)
              
        question_dict = dict()
        question_dict["question_id"] = question_data[0]
        question_dict["user_id"]=question_data[1]
        question_dict["title"]=question_data[2]
        question_dict["body"]=question_data[3]
        question_dict["tag"]=question_data[5]
        question_dict["posted at"]=str(question_data[4])
       
        return question_dict, 200

    @jwt_required
    def delete(self,user_id,questionId):
        current_user = get_jwt_identity()
        db.get_by_parameter('questionstable','user_id',user_id)
    if current_user ==

        db.delete_question(current_user,questionId)

        # db.get_by_parameter('questionstable','user_id',user_id)
        # if user_id == current_user:
            

              
        
        
      
       
class PostAnswer(Resource):
    @jwt_required
    def post(self,questionId):

        parser= reqparse.RequestParser()
        """collecting arguments"""
        parser.add_argument('answerid',type=int,required=True)
        parser.add_argument('content',type=str,required=True)
        

        """getting specific arguments"""

        argument = parser.parse_args()

        answerid = argument['answerid']
        content = argument['content']

        """checking whether the empty answerid feild"""
       
        
        """checking whether the content answerid feild"""
        if  not content:
            return make_response(jsonify(
        {
            'message':'The content is needed for this answer to be posted'  
        }
            ),400)

        for our_list in questions_list:
            if int(questionId) == int (our_list['questionid']):
              
                """creating an object"""
                answerobj = Answer_model(answerid,content,questionId)

                """convert object to JSON"""
                convert_answerobj_data = json.loads(answerobj.my_json())

                """insert into the list"""
                answers_list.append(convert_answerobj_data)
                return {'message': 'answer posted successfully.'}, 201

            return make_response(jsonify({
            'message':'Sorry the question does not exist'
        }),404)




        


