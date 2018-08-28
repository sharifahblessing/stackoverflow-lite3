from flask import Flask, jsonify, make_response
from werkzeug.security import generate_password_hash, \
    check_password_hash
import jwt
import datetime
from flask_restful import Resource, Api, reqparse
from datetime import datetime, timedelta
from app.models import User_model, Question_model, Answer_model
from app.database import Database
import json

questions_list=[]
answers_list=[]
db = Database()
def generate_token(username):
    """Generates the access token to be used as the Authorization header"""

    try:
        # set up a payload with an expiration time
        payload = {
            'exp': datetime.utcnow() + timedelta(minutes=30),
            # international atomic time
            'iat': datetime.utcnow(),
            # default  to user id
            'username': username
        }
        # create the byte string token using the payload and the SECRET key

        token = jwt.encode(
            payload,
            "sdfghjhgfdsfg",
            algorithm='HS256'
        ).decode('UTF-8')
        return token

    except Exception as e:
        # return an error in string format if an exception occurs
        return str(e)


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
        username = str(argument['username']).strip
        password = str(argument['password']).strip


       # if username == "" or len(username) < 3:
        #    return make_response(jsonify({"message": "invalid username, Enter correct username please"}),
                            # 400)

        #if password == "" or password == " " or len(password) < 3:
           # return make_response(jsonify({"message": "Password should be morethan 3 characters"}),
                             #400)

        query_user = db.get_by_parameter('userstable','username',username)
        if not query_user:
            return make_response(jsonify({"message": "User does not exist please signup first"}),
                             404)
        user_obj = User_model(query_user[0],query_user[1],query_user[2],query_user[3])
                
        if  check_password_hash(user_obj.password, password):
            token = generate_token(username)

            return make_response(jsonify({"message": "Login successful",
                                          "token": token }),200)


class Questions (Resource):
    """"method for posting a question"""
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
                                        
        """Query database to check whether question exits"""
        check_question = db.get_by_parameter('questions','title',title)
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
        """creating an object"""
        questionobj = Question_model(*check_question) 

        """convert object to JSON"""
        convert_questionobj_data = json.loads(questionobj.my_json())
                                               
        """insert into the database"""
        db.insert_question_data(title,body,tag)
       
        return make_response(jsonify(
                {
                'message':'Question created successfully', 
                'question':convert_questionobj_data         
            }
            ),201)
        
       
#     def get(self):
#         db_questions = db.get_all('questionstable')
#         #interating through the questions
#         db_questions = (questionstable)

#         questions_list =[]
#         questions_list.append(db_questions)
#         for question in db_questions:
#             Question_model(*questions)
#             return {'questions':Question_model(*questions)},200


# class SingleQuestion(Resource):

#     def get(self,questionId):

#         for our_list in questions_list:
#             if int(questionId) == int (our_list['questionid']):
#                 final_data = {
#                     'questionid' : our_list['questionid'],
#                     'title':our_list['title'],
#                     'body':our_list['body'],
#                     'tag':our_list['tag'],
#                     'time':our_list['time'],
#                     'postedby':our_list['postedby']
#                 }
#                 return {'question': final_data}, 200

#         return make_response(jsonify({
#             'message':'Sorry the question does not exist'
#         }),404)


# class PostAnswer(Resource):
    
#     def post(self,questionId):

#         parser= reqparse.RequestParser()
#         """collecting arguments"""
#         parser.add_argument('answerid',type=int,required=True)
#         parser.add_argument('content',type=str,required=True)
        

#         """getting specific arguments"""

#         argument = parser.parse_args()

#         answerid = argument['answerid']
#         content = argument['content']

#         """checking whether the empty answerid feild"""
       
        
#         """checking whether the content answerid feild"""
#         if  not content:
#             return make_response(jsonify(
#         {
#             'message':'The content is needed for this answer to be posted'  
#         }
#             ),400)

#         for our_list in questions_list:
#             if int(questionId) == int (our_list['questionid']):
              
#                 """creating an object"""
#                 answerobj = Answer_model(answerid,content,questionId)

#                 """convert object to JSON"""
#                 convert_answerobj_data = json.loads(answerobj.my_json())

#                 """insert into the list"""
#                 answers_list.append(convert_answerobj_data)
#                 return {'message': 'answer posted successfully.'}, 201

#             return make_response(jsonify({
#             'message':'Sorry the question does not exist'
#         }),404)




        


