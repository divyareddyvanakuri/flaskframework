from flask import Flask
from app import app
import unittest

class FlaskTestCases(unittest.TestCase):

    def test_home(self):
        tester = app.test_client(self)
        response = tester.get("/")
        self.assertEquals(response.get_data(),b"Hello World")
