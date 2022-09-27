import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category

# Functions built based on the functions of the book project (module).

class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path ="postgres://{}:{}@{}/{}".format('student', 'student','localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

            
        self.new_question = {"question": "Whats your name","answer": "Jorge", "category": 1, "difficulty": 1 }
        self.new_quiz_fail =  { 'previous_questions': [6],
            'quiz_category': {
                'type': 'xx',
                'id': 'x'
            }
        }
        self.new_quiz = {'previous_questions': [6],
            'quiz_category': {
                'type': 'Entertainment',
                'id': '3'
            }
        }
        
        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_get_paginated_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['categories'])
        
    def test_get_page_bad(self):
        res = self.client().get('/questions?page=1000')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        #self.assertEqual(data['message'], 'Bad request')
        
    def test_delete_questions(self):
        res = self.client().delete('/questions/20')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
    
    def test_delete_questions_fail(self):
        res = self.client().delete('/questions/1000')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
    
    def test_create_new_question(self):
        res = self.client().post("/questions", json= self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["questions"])
        self.assertTrue(data["total_questions"])
        
    
    def test_get_category(self):
        res = self.client().get("/categories")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['categories'])
    
    
    def test_questions_for_category(self):
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertNotEqual(len(data['questions']), 0)
        self.assertEqual(data['current_category'], 'Science')

    def test_questions_for_Category_fail(self):
        res = self.client().get('/categories/100/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_quiz(self):
        res = self.client().post('/quizzes', json=self.new_quiz)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['question']['category'], 3)

    def test_quiz_not_found_category(self):

        res = self.client().post('/quizzes', json=self.new_quiz_fail)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        
    
    def search_question(self):
        res = self.client().post('/search', json={"searchTerm": "title"})
        data = json.loads(res.data)

        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])

    def test_invalid_search(self):
        res = self.client().post('/search', json={"searchTerm": "estreça da manha"})
        data = json.loads(res.data)

        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
       
    
# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()