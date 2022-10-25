import unittest
from app import db
from flask import Flask
import os
import json



class AuthTest(unittest.TestCase):

    #setup test
    def setUp(self):
        self.app = Flask(__name__)
        self.app.config.from_object('config.Testing')
        self.client = self.app.test_client
        self.user = {
            "name": "olawale",
            "email": "olawale@mail.com",
            "password": "passw0rd!"
        }

    def test_user_creation(self):
        res = self.client().post('/api/v1/register/', headers={'Content-Type': 'application/json'}, data=json.dumps(self.user))
        self.assertEqual(res.status_code, 201)


if __name__ == '__main__':
    unittest.main()
