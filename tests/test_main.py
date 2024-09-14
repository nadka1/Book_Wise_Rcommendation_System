import unittest
import sys
import os

# Add the project directory to the sys.path to resolve module imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import the app and models from the Main module
from Main.main import app, db
from Main.models import User
from Main.recomm import recom

class FlaskTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_app_exists(self):
        self.assertIsNotNone(app)

    def test_home_page(self):
        result = self.app.get('/')
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'Home', result.data)

    def test_registration(self):
        result = self.app.post('/register', data=dict(
            username='testuser',
            email='testuser@example.com',
            password='password',
            confirm_pswd='password'
        ), follow_redirects=True)
        self.assertIn(b'Account Created', result.data)

    def test_login(self):
        with self.app:
            self.app.post('/register', data=dict(
                username='testuser',
                email='testuser@example.com',
                password='password',
                confirm_pswd='password'
            ))
            result = self.app.post('/login', data=dict(
                email='testuser@example.com',
                password='password'
            ), follow_redirects=True)
            self.assertIn(b'You have been logged in', result.data)

    def test_recommender(self):
        result = self.app.post('/recommender', data=dict(
            bookname='Some Book'
        ), follow_redirects=True)
        self.assertIn(b'Here are the following recommendations', result.data)

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
