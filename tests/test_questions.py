import json

from tests import BaseTestCase

class Tests_Requests(BaseTestCase):
    
      

    """Test for questions"""
    def test_question_submission_successfully(self):
        """Tests when the questions  are submitted successfully"""
        with self.client:
    
            response = self.add_question("1","hello","hello world","java","kenneth")
            self.assertEqual(response.status_code, 201)
                          
    def test_get_all_questions(self):
        """Tests when all question are retrieved successfully"""
        with self.client:
            response = self.get_question()
            self.assertEqual(response.status_code, 200)
           
    def test_get_single_question(self):

       """Tests when single question are retrieved successfully"""
       with self.client:
           
            """first insert a question"""
            response = self.add_question("1","hello","hello world","java","kenneth")
            self.assertEqual(response.status_code, 201)
            """then get a specific question"""
            response = self.get_one_question(1)
            self.assertEqual(response.status_code, 200)

    def test_no_single_question(self):
    
       """Tests when no single question are retrieved successfully"""
       with self.client:
           
            """first insert a question"""
            response = self.add_question("1","hello","hello world","java","kenneth")
            self.assertEqual(response.status_code, 201)
            """then get a specific question"""
            response = self.get_one_question(2)
            self.assertEqual(response.status_code, 404)

    def test_answer_question(self):
        
       """Tests when posted answer"""
       with self.client:
           
            """first insert a question"""
            response = self.add_question("1","hello","hello world","java","kenneth")
            self.assertEqual(response.status_code, 201)
            """then get a specific question to answer"""
            response = self.post_answer(1,"1","try removing errors")
            self.assertEqual(response.status_code, 201)

    def test_no_question_for_your_answer(self):
        
       """Tests when no question for posted answer"""
       with self.client:
           
            """first insert a question"""
            response = self.add_question("1","hello","hello world","java","kenneth")
            self.assertEqual(response.status_code, 201)
            """then get a specific question"""
            response = self.post_answer(23,"1","try removing errors")
            self.assertEqual(response.status_code, 404)

    def test_question_duplicates(self):
        
       """Tests question duplicates"""
       with self.client:
           
            """first insert a question"""
            self.add_question("1","hello","hello world","java","kenneth")
            response = self.add_question("1","hello","hello world","java","kenneth")
            self.assertEqual(response.status_code, 409)
          
            


   