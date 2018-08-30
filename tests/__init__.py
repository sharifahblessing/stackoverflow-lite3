import os
import sys
sys.path.append(os.getcwd())
import unittest
import json
from app import app

from app.views import db


class BaseTestCase(unittest.TestCase):
    


    def create_app(self):
        """
        Create an instance of the app with the testing configuration
        """
        
        return app
        
    def setUp(self):
        self.client = app.test_client(self)

    def signUp(self, name,username, password):
        """
        Function to create a request
        """
        return self.client.post(
            'api/v1/auth/signup',
            data=json.dumps(
                dict(
                    
                    name=name,
                    username=username,
                    password=password
                )
            ),
            content_type='application/json'
        )

    def Login(self,username, password):
        """
        Function to create a request
        """
        return self.client.post(
            'api/v1/auth/login',
            data=json.dumps(
                dict(
                    username=username,
                    password=password
                )
            ),
            content_type='application/json'
        )

    

    def add_question(self, title, body,tag, token):
        """
        Function to add a question
        """
        #/api/v1/questions
        return self.client.post(
            '/api/v1/questions',
            data=json.dumps(
                dict(
                   
                    title=title,
                    body=body,
                    tag=tag
                )
            ),
            content_type='application/json',
             headers=({"token": token})
           
        )

    def get_token(self):
        """Get a token for testing all endpoints"""
        response = self.Login("sharifah", "123456789")
        data = json.loads(response.data)
        return data['token']

    def get_question(self):
        """
        function to return questions
        """
        return self.client.get('/api/v1/questions')

    def get_one_question(self, id):
        """
        function to get one question
        """
        return self.client.get('/api/v1/questions/'+str(id))

    def post_answer(self,question_id,answerid, content):
        
         return self.client.post(
           '/api/v1/questions/'+str(question_id)+'/answers',
            data=json.dumps(
                dict(
                    answerid=answerid,
                    content=content
                )
            ),
            content_type='application/json'
        )

    def delete_one_question(self, id):
        """
        function to get one question
        """
        return self.client.delete('/api/v1/questions/'+str(id))

    def update_answer(self, qid, aid, token):
        """
        functionupdate
        """
        return self.client.put(
            '/api/v1/questions/"'+str(qid)+'"/answers/'+str(aid),
            data=json.dumps(               
                   
                    {'content':content}
                
            ),
            content_type='application/json'
            ,
            headers=({"token": token})
        )