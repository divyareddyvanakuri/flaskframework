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
    
    def test_for_database_connetion_then_itShould_returns_done(self):
        tester = app.test_client(self)
        response = tester.get("/database",content_type='html/text')
        self.assertEqual(response.get_data(),b"Done!")

    def test_for_already_existed_table(self):
        tester = app.test_client(self)
        response = tester.get("/database",content_type='html/text')
        self.assertEqual(response.get_data(),b"Table already existed")


if  __name__ == "__main__":
    unittest.main()