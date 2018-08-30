import datetime
from flask import Flask, jsonify, make_response
from werkzeug.security import generate_password_hash, \
    check_password_hash
import jwt
import psycopg2
from flask_restful import Resource, Api, reqparse
from datetime import datetime, timedelta
from app.models import User_model, Question_model, Answer_model
from app.database import Database
import json
from app.config import generate_token, decode_token


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

        try :

        
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

        except psycopg2.DatabaseError as e:
            if db.connection:
                db.connection.rollback()
                print(e)
        
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


        query_user = db.get_by_parameter('userstable','username',username)
        print(query_user)
        if  query_user:
            
            user_obj = User_model(query_user[0],query_user[1],query_user[2],query_user[3])
            print(user_obj)
            print(check_password_hash(user_obj.password, password))
                    
            if  check_password_hash(user_obj.password, password):
                token = generate_token(username)
                
                return make_response(jsonify({"message": "Login successful",
                                            "token": token,
                                            
                                             }),200)
        return make_response(jsonify({"message": "User does not exist please signup first"}),
                             404)

class Questions (Resource):
    """"method for posting a question"""
    
    def post(self):
        parser= reqparse.RequestParser()

        """collecting arguments"""
        parser.add_argument('title',required=True)
        parser.add_argument('body',type=str,required=True)
        parser.add_argument('tag',type=str,required=True)
        parser.add_argument('token', location='headers')

        """getting specific arguments"""

        argument = parser.parse_args()

        title = str(argument['title']).strip()
        body = argument['body']
        tag = argument['tag']
        
        token = argument['token']

        if not token:
            return make_response(jsonify({
                'message':'token missing'
            }),400)

        """ implementing token decoding"""
        decoded = decode_token(token)
        if decoded["status"] == "Failure":
            return make_response(jsonify({"message": decoded["message"]}),
                                 401)
                                        
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
        
        try:

            """insert into the database"""
            db.insert_question_data(1, title,body,tag)
        
            return make_response(jsonify(
                    {
                    'message':'Question created successfully'}
                    
                ),201)
        except psycopg2.DatabaseError as e:
            if db.connection:
                db.connection.rollback()
                print(e)
        
       
    def get(self):
        try:
            db_questions = db.get_all('questionstable')
            
            if db_questions:
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
            return make_response(jsonify({'message':'No questions yet'}),404)

        except psycopg2.DatabaseError as e:

            if db.connection:
                db.connection.rollback()
                print(e)

class SingleQuestion(Resource):
    
    def get(self,questionId):
        try:
        
            question_data = db.get_by_parameter('questionstable','questionid',questionId)
            if question_data:
                
                question_dict = dict()
                question_dict["question_id"] = question_data[0]
                question_dict["user_id"]=question_data[1]
                question_dict["title"]=question_data[2]
                question_dict["body"]=question_data[3]
                question_dict["tag"]=question_data[5]
                question_dict["posted at"]=str(question_data[4])
            
                return str(question_dict), 200
            return make_response(jsonify({'message':'question doesnot exist'}),404)

        except psycopg2.DatabaseError as e:

            if db.connection:
                db.connection.rollback()
                print(e)
    
    def delete(self,questionId):
        parser = reqparse.RequestParser()
        parser.add_argument('token', location='headers')

        argument = parser.parse_args()   
        token = argument['token']


        if not token:
            return make_response(jsonify({
                'message':'token missing'
            }),400)

        """ implementing token decoding"""
        decoded = decode_token(token)
        if decoded["status"] == "Failure":
            return make_response(jsonify({"message": decoded["message"]}),
                                 401)

        try:

            if db.delete_question(owner,questionId):
                return{
                    "message":"delete successful"
                },202

            return{"message":"delete error"},400

        except psycopg2.DatabaseError as e:

            if db.connection:
                db.connection.rollback()
                print(e)

       
class PostAnswer(Resource):
       
    def post(self,questionId): 
             
              
        parser= reqparse.RequestParser()

        """collecting arguments"""
        parser.add_argument('content',required=True)
        parser.add_argument('token', location='headers')
       
        """getting specific arguments"""

        argument = parser.parse_args()        
        content = argument['content']  
        token = argument['token']   

        if not token:
            return make_response(jsonify({
                'message':'token missing'
            }),400)

        """ implementing token decoding"""
        decoded = decode_token(token)
        if decoded["status"] == "Failure":
            return make_response(jsonify({"message": decoded["message"]}),
                                 401)

        try:

         
            """Query database to check whether answer exits"""
            check_answer = db.get_by_parameter('answerstable','content',content)
            if  check_answer:
                return make_response(jsonify(
                {
                'message':'This answer already exists'}
                ),409)
            if  not content:
                return make_response(jsonify(
            {
                'message':'The content is needed for this answer to be posted'  
            }
                ),400)  

            """get a user via the question """
            user_via_question = db.get_by_parameter('questionstable','questionid',questionId)

            question_dict = dict()
            """get a user id """
            question_dict["user_id"]= user_via_question[1]
            user_id = question_dict["user_id"]

            """insert into the database"""
            db.insert_answer_data(user_id,questionId,content)
        
            return make_response(jsonify(
                    {
                    'message':'Answer created successfully'}
                    
                ),201)
        except psycopg2.DatabaseError as e:

            if db.connection:
                db.connection.rollback()
                print(e)
        
class UpdateAnswer(Resource):

   
    def put(self,questionId,answerId):  
              
        parser= reqparse.RequestParser()

        """collecting arguments"""
        parser.add_argument('content',required=True)
        parser.add_argument('token', location='headers')
       
        """getting specific arguments"""

        argument = parser.parse_args()        
        content = argument['content']   
        token = argument['token']  
  
        if not token:
            return make_response(jsonify({
                'message':'token missing'
            }),400)

        """ implementing token decoding"""
        decoded = decode_token(token)
        if decoded["status"] == "Failure":
            return make_response(jsonify({"message": decoded["message"]}),
                                 401)

        try:

            """insert into the database"""
            db.update_answer_data(answerId, questionId,content)
        
            return make_response(jsonify(
                    {
                    'message':'Answer  updated  successfully'}
                    
                ),201)
        except psycopg2.DatabaseError as e:

            if db.connection:
                db.connection.rollback()
                print(e)

        
