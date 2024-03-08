import unittest
from unittest.mock import Mock
from main import *

print("Running test_my_module...")

class TestMain(unittest.TestCase):
    # def test_AddUser(self):
     #   new_person = User(First_name="moshe", Last_name="bercovici", Email="moses@meatmoses.com", Password="123456",
      #              City="beer sheva", Age=25, Proficiency="doctor", Role="admin", Last_login=func.now())
       # self.assertEquals()

    #def test_AddRequest(self):
        # Test the "/Add_Request" endpoint
     #   request_data = {
      #      "name": "John",
       #     "city": "New York",
        #    "problem": "Some problem description",
         #   "additionalRequests": "Additional details"
        #}
        #response = self.client.post("/api/Add_Request", json=request_data)
        #self.assertEqual(response.status_code, 200)
        #self.assertEqual(response.json(), {"status": "success", "message": "Request added successfully"})
    print("in the class")
    # class TestMyModule(unittest.TestCase):
    def setUp(self):
        # Initialize a mock database session
        self.db = Mock()

    def test_get_request_existing(self):
        # Assuming a valid request ID
        request = {"id_request": 123}
        result = get_request(request, self.db)
        self.assertIsNotNone(result)

    def test_get_request_nonexistent(self):
        # Assuming an invalid request ID
        request = {"id_request": 999}
        result = get_request(request, self.db)
        self.assertIsNone(result)

    def test_approve_existing_request(self):
        # Assuming a valid request
        request = {"id_request": 123}
        result = approve_request(request, self.db)
        self.assertEqual(result["message"], "Request updated successfully")

    def test_approve_nonexistent_request(self):
        # Assuming an invalid request
        request = {"id_request": 999}
        with self.assertRaises(HTTPException):
            approve_request(request, self.db)

    def test_deny_existing_request(self):
        # Assuming a valid request
        request = {"id_request": 123}
        result = deny_request(request, self.db)
        self.assertEqual(result["message"], "Request removed successfully")

    def test_deny_nonexistent_request(self):
        # Assuming an invalid request
        request = {"id_request": 999}
        with self.assertRaises(HTTPException):
            deny_request(request, self.db)