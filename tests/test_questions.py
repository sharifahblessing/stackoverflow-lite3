import json
import datetime
from tests import BaseTestCase

class Tests_Requests(BaseTestCase):

    def test_signing_up_users(self):
        """Tests when user signs up"""
        with self.client:
            """auto generate usernames with the help of system  date time"""
            autogenerate_usernames = str(datetime.datetime.now())
            response = self.signUp('sharifah','sharifah'+autogenerate_usernames, '123456789')
            """getting the response  from data"""
            self.assertEqual(response.status_code, 201)

    def test_login_user(self):
         """Tests user when logging in"""
         """first signup"""
         self.signUp('sharifah','sharifah', '123456789')
         """Then login"""
         response = self.Login('sharifah','123456789')
         """getting the response  from data"""
         self.assertEqual(response.status_code, 200)

    def test_add_questions(self):
        """Tests when entering an question."""
        """auto generate questions with the help of system  date time"""
        autogenerate_question = str(datetime.datetime.now())
        token = self.get_token()
        response = self.add_question("my programming"+autogenerate_question," programming is good"+autogenerate_question,"programming",token)
        self.assertEqual(response.status_code, 201)
    

    def test_get_questions(self):
        """Tests get question."""
        autogenerate_question = str(datetime.datetime.now())
        token = self.get_token()
        response = self.add_question("my programming"+autogenerate_question," programming is good"+autogenerate_question,"programming",token)
        response = self.get_question()
        self.assertEqual(response.status_code, 200)

    def test_get_single_question(self):
        """Tests get single question."""
        autogenerate_question = str(datetime.datetime.now())
        token = self.get_token()
        response = self.add_question("my programming"+autogenerate_question," programming is good"+autogenerate_question,"programming",token)
        response = self.get_one_question(1)
        self.assertEqual(response.status_code, 200)

    def test_delete_single_question_problem(self):
        """Tests delete single question problem."""
        autogenerate_question = str(datetime.datetime.now())
        token = self.get_token()
        response = self.add_question("my programming"+autogenerate_question," programming is good"+autogenerate_question,"programming",token)
        response = self.delete_one_question(1)
        self.assertEqual(response.status_code, 400)
   
    def test_update_answer(self):

        """Tests update answer."""
        autogenerate_question = str(datetime.datetime.now())
        token = self.get_token()
        response = self.add_question("my programming"+autogenerate_question," programming is good"+autogenerate_question,"programming",token)
        response = self.update_answer(1,1,token)
        self.assertEqual(response.status_code, 201)


    