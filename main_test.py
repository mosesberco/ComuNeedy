import unittest
import asyncio
from unittest.mock import Mock
import main
from main import *


class TestMain(unittest.TestCase):
    def setUp(self):
        self.db = Mock()

    def test_add_new_request(self):
        # Proper dict matching function's expected keys
        new_request_dict = {
            'name': "moses",
            'city': "Beersheva",
            'problem': "data",
            'datetime': "2024-03-08T12:00:00",  # Replace with a valid datetime string
            'additionalRequests': "Additional_Requests"
        }

        result = add_request(new_request_dict, self.db)
        self.assertEqual(result.get('message'), "Request added successfully")

    def test_2_add_new_request(self):
        # dict with wrong key
        new_request_dict = {
            'Email_asker': "mosesberco1@gmail.com",
            'First_name': "moses",
            'Information': "data",
            'Availability': func.now(),
            'Additional_Requests': "Additional_Requests"
        }
        with self.assertRaises(HTTPException):
            add_request(new_request_dict, self.db)

    def test_3_add_new_request(self):
        new_request_dict = {
            # dict with int instead of string
            'Email_asker': "mosesberco1@gmail.com",
            'First_name': 123,
            'Information': "data",
            'Availability': func.now(),
            'Additional_Requests': "Additional_Requests"
        }
        with self.assertRaises(HTTPException):
            add_request(new_request_dict, self.db)


    def test_4_add_new_request(self):
        # dict without all of the needed filed
        new_request_dict = {
            'First_name': 123,
            'Information': "data",
            'Availability': func.now(),
            'Additional_Requests': "Additional_Requests"
        }
        with self.assertRaises(HTTPException):
            add_request(new_request_dict, self.db)


