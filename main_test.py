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

    def test_approve_invalid_request_id01(self):
        # Assuming an invalid request - id is str instead int
        request = {"id_request": 'abc'}
        with self.assertRaises(HTTPException):
            asyncio.run(approve_request(request, self.db))

    def test_approve_invalid_request_id02(self):
        # Assuming an invalid request ID - id is float instead int
        request = {"id_request": 1.5}
        with self.assertRaises(HTTPException):
            asyncio.run(approve_request(request, self.db))

    def test_approve_invalid_request_id03(self):
        # Assuming an invalid request ID - dict is empty
        request = {}
        with self.assertRaises(HTTPException):
            asyncio.run(approve_request(request, self.db))

    def test_deny_existing_request(self):
        # Assuming a valid request
        request = {"id_request": 123}
        result = asyncio.run(deny_request(request, self.db))
        self.assertEqual(result.get("message"), "Request removed successfully")

    def test_deny_invalid_request_id01(self):
        # Assuming an invalid request - id is str instead int
        request = {"id_request": 'abc'}
        with self.assertRaises(HTTPException):
            asyncio.run(deny_request(request, self.db))

    def test_deny_invalid_request_id02(self):
        # Assuming an invalid request ID - id is float instead int
        request = {"id_request": 4.2}
        with self.assertRaises(HTTPException):
            asyncio.run(deny_request(request, self.db))

    def test_deny_invalid_request_id03(self):
        # Assuming an invalid request ID - dict is empty
        request = {}
        with self.assertRaises(HTTPException):
            asyncio.run(deny_request(request, self.db))
