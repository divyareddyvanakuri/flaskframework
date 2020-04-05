from flask import Flask
from app import app
import unittest

class FlaskTestCases(unittest.TestCase):

    def test_home(self):
        tester = app.test_client(self)
        response = tester.get("/")
        self.assertEqual(response.get_data(),b"Hello World")

    def test_login(self):
        tester = app.test_client(self)
        response = tester.get("/login",content_type='html/text')
        self.assertEqual(response.get_data(),b"Please login")

    def test_register(self):
        tester = app.test_client(self)
        response = tester.get("/register",content_type='html/text')
        self.assertEqual(response.get_data(),b"Please register")

if  __name__ == "__main__":
    unittest.main()