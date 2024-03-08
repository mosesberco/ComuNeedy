from fastapi.testclient import TestClient
import unittest
from main import *


class TestMain(unittest.TestCase):
    
    
    def setUp(self):
        self.client = TestClient(app)
    
    
    #unit test added by ariel for add user.
    def test_add_user(self):
        # Test the "/add_user" endpoint
        user_data = {
            "First_name": "Ariel",
            "Last_name": "Perstin",
            "Email": "xcvxv@gmail.com",
            "Password": "123456",
            "City": "Beer Sheva",
            "Age": 22,
            "Proficiency": "Skiller",
            "Role": "User"
        }
        response = self.client.post("/api/add_user", json=user_data)
        assert response.status_code == 200 
        assert response.json()["message"] == "User added successfully"
    

    
    #another 3 unit tests added by AI (Claude)
    def test_add_user_duplicate_email(self):
        # Test with an existing email
        existing_user_data = {
            "First_name": "Ariel",
            "Last_name": "Perstin",
            "Email": "arielperstin10@gmail.com",
            "Password": "123",
            "City": "Beer Sheva",
            "Age": 22,
            "Proficiency": "Electric",
            "Role": "User"
        }
        self.client.post("/api/add_user", json=existing_user_data)

        # Attempt to create a new user with the same email
        duplicate_user_data = {
            "First_name": "Eran",
            "Last_name": "Cohen",
            "Email": "arielperstin10@gmail.com",
            "Password": "123",
            "City": "Haifa",
            "Age": 35,
            "Proficiency": "Trainer",
            "Role": "Volunteer"
        }
        response = self.client.post("/api/add_user", json=duplicate_user_data)
        assert response.status_code == 400
        assert response.json()["detail"] == "The email is already existing"
    


    
    def test_add_user_missing_required_fields(self):
        # Test with missing required fields
        incomplete_user_data = {
            "First_name": "Alice",
            "Last_name": "Smith",
            "Email": "alicesmith@example.com",
            "Password": "password789",
            "City": "Chicago",
            # Age and Proficiency fields are missing
            "Role": "User"
        }
        response = self.client.post("/api/add_user", json=incomplete_user_data)
        assert response.status_code == 400  # Unprocessable Entity
        
    

    
    def test_add_user_invalid_data_types(self):
        # Test with invalid data types
        invalid_user_data = {
            "First_name": 123,
            "Last_name": True,
            "Email": "invalid@email",
            "Password": 456,
            "City": 789,
            "Age": "thirty",
            "Proficiency": None,
            "Role": "Admin"
        }
        response = self.client.post("/api/add_user", json=invalid_user_data)
        assert response.status_code == 400  # Unprocessable Entity
        
    

    
if __name__ == '__main__':
    unittest.main()