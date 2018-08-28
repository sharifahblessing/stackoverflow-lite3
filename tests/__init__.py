import os
import sys
sys.path.append(os.getcwd())
import unittest
import json
from app import app, config
from app.config import app_config
from app.views import questions_list,answers_list


class BaseTestCase(unittest.TestCase):
    def create_app(self):
        """
        Create an instance of the app with the testing configuration
        """
        app.config.from_object(app_config["testing"])
        return app

    def setUp(self):
        self.client = app.test_client(self)

    def tearDown(self):
        """
        Drop the data structure data
        """
        questions_list[:] = []
        answers_list[:] = []

    def add_question(self, questionid, title, body,tag, postedby):
        """
        Function to add a question
        """
        return self.client.post(
            '/api/v1/questions',
            data=json.dumps(
                dict(
                    questionid=questionid,
                    title=title,
                    body=body,
                    tag=tag,
                    postedby=postedby
                )
            ),
            content_type='application/json'
        )
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
        

   







