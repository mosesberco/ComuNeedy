import unittest
from unittest.mock import Mock
from main import *
import asyncio
class TestMain(unittest.TestCase):
    def setUp(self):
        # Initialize a mock database session
        self.db = Mock()

    def test_approve_existing_request(self):
        # Assuming a valid request
        request = {"id_request": 123}
        result = asyncio.run(approve_request(request, self.db))
        self.assertEqual(result.get("message"), "Request updated successfully")

    def test_approve_nonexistent_request(self):
        # Assuming an invalid request
        request = {"id_request": 'abc'}
        with self.assertRaises(HTTPException):
            asyncio.run(approve_request(request, self.db))

    def test_deny_existing_request(self):
        # Assuming a valid request
        request = {"id_request": 123}
        result = asyncio.run(deny_request(request, self.db))
        self.assertEqual(result.get("message"), "Request removed successfully")

    def test_deny_nonexistent_request(self):
        # Assuming an invalid request
        request = {"id_request": 'abc'}
        with self.assertRaises(HTTPException):
            asyncio.run(deny_request(request, self.db))